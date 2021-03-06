# Python imports
import logging

# ONSA imports
from charles.utils.utils import *
from charles.utils.inventory_utils import *
from charles.utils.ipam_utils import *
from charles.constants import *
from charles.models import *


def deleted_automated_request(service):
  logging.debug("deleted_automated_request")
  client = get_client(service['client_id'])
  service_data = {}

  try:
    parameters = an_parameters(client, service)
    config = {
      "client": client['name'],
      "service_type":  service['service_type'],
      "service_id": service['service_id'],
      "op_type": "DELETE"}

    config['parameters'] = {
                "service_vlan": service['vlan_id'],
                "an_client_port": parameters['an_client_port'],
                "an_uplink_ports": parameters['an_uplink_ports'],
                "access_port_services":parameters['access_port_services']
                  }
    config['devices'] = [{"vendor": parameters['vendor'],
        "model": parameters['model'], "mgmt_ip": parameters['mgmt_ip']}]

    service_state = DELETEINPROGRESS_SERVICE_STATE

    logging.debug(f'releasing service resources for service {service}')
    if service['public_network']:
      destroy_subnet(client['name'], service['service_id'])
    if service['wan_network']:
      destroy_subnet(client['name'], service['service_id'])
    release_access_port(service['access_port_id'])
    release_vlan(service['access_node_id'], service['vlan_id'])
    logging.debug("deleting service")

    #Send message(job) to Queue so workers can take it
    configure_service(config) 
  except BaseException as e:
    logging.error(e)
    service_state = DELETEERROR_SERVICE_STATE

  service_data['service_state'] = service_state
  update_jeangrey_service(service['service_id'], service_data)
  service = update_charles_service(service, service_state)
  return service


def an_activated_automated_request(service):
  logging.debug("an_activated_automated_request")
  client = get_client(service['client_id'])
  service_data = {}

  try:
    parameters = an_parameters(client, service)
    config = {
      "client": client['name'],
      "service_type":  service['service_type'],
      "service_id": service['service_id'],
      "op_type": "CREATE"}

    backbone_parameters = bb_parameters(client, service)

    config['parameters'] = {
                "service_vlan": service['vlan_id'],
                "an_client_port": parameters['an_client_port'],
                "an_uplink_ports": parameters['an_uplink_ports'],
                "access_port_services":parameters['access_port_services']
                  }
    config['devices'] = [{"vendor": parameters['vendor'],
        "model": parameters['model'], "mgmt_ip": parameters['mgmt_ip']}]

    service_state = "an_activation_in_progress"
    logging.debug("configuring service")
    
    #Send message(job) to Queue so workers can take it
    configure_service(config) 
  except BaseException:
    service_state = "ERROR"
    destroy_subnet(client['name'], service['service_id'])

  service_data['service_state'] = service_state
  service_data['public_network'] = backbone_parameters['public_network']
  service_data['wan_network'] = backbone_parameters['wan_network']
  update_jeangrey_service(service['service_id'], service_data)
  service = update_charles_service(service, service_state)
  return service

def an_parameters(client, service):
  try:
    access_port = get_access_port(service['access_port_id'])
    access_node = get_access_node(service['access_node_id'])
    an_device_model = get_device_model(access_node['device_model_id'])
    access_port_services = get_access_port_services(service['access_port_id'])

    services = ""
    for my_service in access_port_services:
      if my_service['id'] is not service['service_id']:
        services+= str(my_service['id']) + "-"
    services += str(service['service_id'])

    parameters = { 'provider_vlan': access_node['provider_vlan'],
                  'an_client_port': access_port['port'],
                  'an_uplink_ports': access_node['uplink_ports'],
                  'mgmt_ip': access_node['mgmt_ip'],
                  'model': an_device_model['model'],
                  'vendor': an_device_model['brand'],
                  'access_port_services': services }

    logging.debug(f'parameters: {parameters}')

    return parameters
  except BaseException:
    logging.error("Unable to fetch parameters")
    raise InvalidParametersException("Unable to fetch parameters")

  # service_data = {}



def bb_parameters(client, service):
  try:
    location = get_location(service['location_id'])
    logging.debug(f'location: {location}')

    router_node = get_router_node(service['router_node_id'])
    logging.debug(f'router_node: {router_node}')

    rn_device_model = get_device_model(router_node['device_model_id'])
    
    logging.debug(f'looking network with prefix {service["prefix"]} for service ID {service["service_id"]} client {client["name"]}')
    public_network = assign_network(client['name'], service['service_id'],IPAM_PUBLIC_NETWORK,service['prefix'])
    logging.debug(f'network: {public_network}')
    wan_network = assign_network(client['name'], service['service_id'],IPAM_MGMT_WAN,IPAM_MGMT_WANPREFIX)
    logging.debug(f'network: {wan_network}')

    parameters = {
                'pop_size': location['pop_size'],
                'public_network' : public_network,
                'wan_network' : wan_network
                }

    parameters['router_node'] = { 'vendor': rn_device_model['brand'],
                                  'model': rn_device_model['model'],
                                  'mgmt_ip': router_node['mgmt_ip']
                                }

    logging.debug(f'parameters: {parameters}')
    return parameters
  except BaseException:
    logging.error("Unable to fetch parameters")
    raise InvalidParametersException("Unable to fetch parameters")


    # """
    # Fetch  logical units
    # """
    # if service['logical_unit_id'] is None:
    #   free_logical_units = get_free_logical_units(router_node['id'])
    #   if free_logical_units is None:
    #       logging.warning('No available logical units')
    #       parameters['status'] = ERR_NO_LOGICALUNITS
    #       return parameters
    #   else:
    #       logical_unit_id = free_logical_units[0]['id']
    #       client_network = get_client_network(client['name'], service['id'], service['prefix'])
    #       if client_network:
    #           add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
    #       else:
    #           logging.warning('No public networks available')
    #           parameters['status'] = ERR_NO_PUBLICNETWORKS
    #           return parameters

    #   wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])

    # else:
    #   logical_unit_id = service['logical_unit_id']
    #   client_network = service['public_network']
    #   wan_network = service['wan_network']



def bb_data_ack_automated_request(service):
  # if DEBUG: print("bb_data_ack_automated_request")
  # client = get_client(service['client_id'])
  # parameters = bb_parameters(client, service)

  # if DEBUG: print(parameters)

  # #Handle parameters ERROR
  # if parameters is not None:
  #   service_data = {  'logical_unit_id': parameters['logical_unit_id'],
  #                     'wan_network':  parameters['wan_network']
  #                   }
  #   service_data['public_network'] = parameters['client_network']
  #   service_state = "bb_data_ack"

  # else:
  #   service_data = {}
  #   service_state = "ERROR"

  # service_data['service_state']=service_state
  # update_jeangrey_service(service['service_id'], service_data)
  # service = update_charles_service(service, service_state)
  # service.update(service_data)
  # my_service = service
  # return my_service
  pass


def bb_activated_automated_request(service):
  # if DEBUG: print("bb_activated_automated_request")
  # client = get_client(service['client_id'])
  # parameters = bb_parameters(client, service)

  # config = {
  #      "client" : client['name'],
  #      "service_type" :  service['service_type'],
  #      "service_id" : service['service_id'],
  #      "op_type" : "CREATE" }

  # config['parameters'] =  {
  #                         "pop_size" : parameters['pop_size'],       
  #                         "an_uplink_interface" : parameters['an_uplink_interface'],
  #                         "an_uplink_ports" :   parameters['an_uplink_ports'],
  #                         "logical_unit" : parameters['logical_unit_id'],   
  #                         "provider_vlan" : parameters['provider_vlan'],      
  #                         "service_vlan" : service['vlan_id'], 
  #                         "an_client_port" : parameters['an_client_port'],
  #                         "wan_cidr": service['wan_network'],
  #                         "client_cidr": service['public_network']
  #                         }

  # config['devices'] =  [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']}]

  # configure_service(config)
  # # service_data = {}
  # # service_data['service_state'] = "bb_activation_in_progress"
  # service_state = "bb_activation_in_progress"
  # service_data = {'service_state' : service_state}
  # update_jeangrey_service(service['service_id'], service_data)
  # service = update_charles_service(service, service_state)

  # return service
  pass

def an_data_ack_automated_request(service):
  # if DEBUG: print("an_data_ack_automated_request")
  # # service_data = {}
  # # service_data['service_state'] = "an_data_ack"
  # service_state = "an_data_ack"
  # service_data = {'service_state' : service_state}
  # update_jeangrey_service(service['service_id'], service_data)
  # service = update_charles_service(service, service_state)
  # return service
  pass


def cpe_data_ack_automated_request(service):
  # if DEBUG: print("cpe_data_ack_automated_request")
  # client = get_client(service['client_id'])
  # parameters = cpe_parameters(client, service)
  # customer_location = get_customer_location(service['client_id'], service['customer_location_id'])

  # if parameters['client_port_id']:
  #   service_data = { "client_port_id": parameters['client_port_id']}

  # service_state = "cpe_data_ack"

  # service_data['service_state']=service_state
  # update_jeangrey_service(service['service_id'], service_data)
  # service = update_charles_service(service, service_state)  
  # service.update(service_data)
  # return service
  pass

def service_activated_automated_request(service):
  # if DEBUG: print("service_activated_automated_request")
  # client = get_client(service['client_id'])
  # parameters = cpe_parameters(client, service)
  # config = {
  #    "client" : client['name'],
  #    "service_type" :  service['service_type'],
  #    "service_id" : service['service_id'],
  #    "op_type" : "CREATE" }

  # service_data = {}

  # if parameters is not None:
  #   config['parameters'] =  {  
  #               "service_vlan" : service['vlan_id'], 
  #               "bandwidth" : service['bandwidth'],
  #               "on_client_port" : parameters['client_node']['interface_name'],
  #               "on_uplink_port" : parameters['client_node']['uplink_port'],
  #               "wan_cidr": service['wan_network'],
  #               "client_cidr": service['public_network']
  #              }

  #   config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


  #   service_state = "cpe_activation_in_progress"
  #   configure_service(config)
  # else:
  #   service_state = "ERROR"

  # service_data['service_state'] = service_state
  # update_jeangrey_service(service['service_id'], service_data)
  # service = update_charles_service(service, service_state)  
  # return service
  pass


def cpe_parameters(client, service):
  pass 
  # location = get_location(service['location_id'])
  # client_node = get_client_node(service['client_node_sn'])
  # parameters = {}
  
  # if service['client_port_id'] is None:
  #   customer_location = get_customer_location(client['id'],service['customer_location_id'])
  #   client_port_id = fetch_cpe_port_id(service['client_node_sn'], client['name'], customer_location)      
  #   client_port = get_client_port(service['client_node_sn'], client_port_id)
  #   parameters['client_port_id'] = client_port_id

  # else:
  #   client_port = get_client_port(service['client_node_sn'], service['client_port_id'])

  # parameters['client_node'] = { 'vendor': client_node['vendor'],
  #                               'model': client_node['model'],
  #                               'mgmt_ip': client_node['mgmt_ip'],
  #                               'interface_name': client_port['interface_name'],
  #                               'wan_network': service['wan_network'],
  #                               'uplink_port' : client_node['uplink_port']
  #                             }

  # return parameters