# Python imports
import logging
from pprint import pprint

# ONSA imports
from charles.utils.utils import *
from charles.constants import *

logging.basicConfig(level=logging.DEBUG)
DEBUG = True

def bb_data_ack_automated_request(service):
  if DEBUG: print("bb_data_ack_automated_request")
  client = get_client(service['client_id'])
  parameters = bb_parameters(client, service)

  if DEBUG: print(parameters)

  #Handle parameters error
  if parameters is not None:
    service_data = {  'logical_unit_id': parameters['logical_unit_id'],
                      'wan_network':  parameters['wan_network']
                    }
    service_data['public_network'] = parameters['client_network']
    service_data['service_state'] = "bb_data_ack"


  else:
    service_data['service_state'] = "error"

  update_service(service['service_id'], service_data)
  return service_data['service_state']



def bb_activated_automated_request(service):
  if DEBUG: print("bb_activated_automated_request")
  client = get_client(service['client_id'])
  parameters = bb_parameters(client, service)

  config = {
       "client" : client['name'],
       "service_type" :  service['service_type'],
       "service_id" : service['service_id'],
       "op_type" : "CREATE" }

  config['parameters'] =  {
                          "pop_size" : parameters['pop_size'],       
                          "an_uplink_interface" : parameters['an_uplink_interface'],
                          "an_uplink_ports" :   parameters['an_uplink_ports'],
                          "logical_unit" : parameters['logical_unit_id'],   
                          "provider_vlan" : parameters['provider_vlan'],      
                          "service_vlan" : service['vlan_id'], 
                          "an_client_port" : parameters['an_client_port'],
                          "wan_cidr": service['wan_network'],
                          "client_cidr": service['public_network']
                          }

  config['devices'] =  [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']}]

  configure_service(config)
  service_data = {}
  service_data['service_state'] = "bb_activation_in_progress"
  update_service(service['service_id'], service_data)
  return service_data['service_state']



def an_data_ack_automated_request(service):
  if DEBUG: print("an_data_ack_automated_request")
  service_data = {}
  service_data['service_state'] = "an_data_ack"
  update_service(service['service_id'], service_data)
  return service_data['service_state']



def an_activated_automated_request(service):
  if DEBUG: print("an_activated_automated_request")
  client = get_client(service['client_id'])
  parameters = an_parameters(client, service) 
  service_data = {}

  config = {
     "client" : client['name'],
     "service_type" :  service['service_type'],
     "service_id" : service['service_id'],
     "op_type" : "CREATE" }
  
  if parameters is not None:  
    config['parameters'] =  {  
                "service_vlan" : service['vlan_id'], 
                "an_client_port": parameters['an_client_port']
                  }
    config['devices'] = [{"vendor": parameters['vendor'], "model": parameters['model'], "mgmt_ip": parameters['mgmt_ip']}]

    configure_service(config)
    service_data['service_state'] = "an_activation_in_progress"
    configure_service(config) 

  else:
    service_data['service_state'] = "error"

  update_service(service['service_id'], service_data)
  return service_data['service_state']



def cpe_data_ack_automated_request(service):
  if DEBUG: print("cpe_data_ack_automated_request")
  client = get_client(service['client_id'])
  parameters = cpe_parameters(client, service)
  customer_location = get_customer_location(service['client_id'], service['customer_location_id'])

  if parameters['client_port_id']:
    service_data = { "client_port_id": parameters['client_port_id']}

  service_data['service_state'] = "cpe_data_ack"
  update_service(service['service_id'], service_data)
  return service_data['service_state']


def service_activated_automated_request(service):
  if DEBUG: print("service_activated_automated_request")
  client = get_client(service['client_id'])
  parameters = cpe_parameters(client, service)
  config = {
     "client" : client['name'],
     "service_type" :  service['service_type'],
     "service_id" : service['service_id'],
     "op_type" : "CREATE" }


  service_data = {}

  if parameters is not None:
    config['parameters'] =  {  
                "service_vlan" : service['vlan_id'], 
                "bandwidth" : service['bandwidth'],
                "on_client_port" : parameters['client_node']['interface_name'],
                "on_uplink_port" : parameters['client_node']['uplink_port'],
                "wan_cidr": service['wan_network'],
                "client_cidr": service['public_network']
               }

    config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


    service_data['service_state'] = "cpe_activation_in_progress"
    configure_service(config)
  else:
    service_data['service_state'] = "error"
  
  update_service(service['service_id'], service_data)
  return service_data['service_state']

def bb_parameters(client, service):
    location = get_location(service['location_id'])
    router_node = get_router_node(service['router_node_id'])
    access_port = get_access_port(service['access_port_id'])
    access_node = get_access_node(service['access_node_id'])

    """
    Fetch for logical units
    """
    if service['logical_unit_id'] is None:
      free_logical_units = get_free_logical_units(router_node['id'])
      if (free_logical_units == 524):
          logging.warning('No available logical units')
          return free_logical_units
      else:
          logical_unit_id = free_logical_units[0]['logical_unit_id']
          client_network = get_client_network(client['name'], service['id'], service['prefix'])
          if client_network:
              add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
          else:
              logging.warning('No public networks available')
              return ERR541

      wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])

    else:
      logical_unit_id = service['logical_unit_id']
      client_network = service['public_network']
      wan_network = service['wan_network']

    parameters = {
                 'pop_size': location['pop_size'],
                 'an_uplink_interface' : access_node['uplink_interface'],
                 'an_uplink_ports' :   access_node['uplink_ports'],
                 'logical_unit_id': logical_unit_id,   
                 'provider_vlan' : access_node['provider_vlan'],      
                 'an_client_port' : access_port['port'],
                 'client_network' : client_network,
                 'wan_network' : wan_network
                 }

    parameters['router_node'] = { 'vendor': router_node['vendor'],
                                  'model': router_node['model'],
                                  'mgmt_ip': router_node['mgmt_ip']
                                }

    return parameters



def cpe_parameters(client, service):
  location = get_location(service['location_id'])
  client_node = get_client_node(service['client_node_sn'])
  parameters = {}
  
  if service['client_port_id'] is None:
    customer_location = get_customer_location(client['id'],service['customer_location_id']) 
    client_port_id = fetch_cpe_port_id(service['client_node_sn'], client['name'], customer_location)
    if (client_port_id == 523):
      return client_port_id
    else:
      client_port = get_client_port(service['client_node_sn'], client_port_id)
      parameters['client_port_id'] = client_port_id

  else:
    client_port = get_client_port(service['client_node_sn'], service['client_port_id'])

  parameters['client_node'] = { 'vendor': client_node['vendor'],
                                'model': client_node['model'],
                                'mgmt_ip': client_node['mgmt_ip'],
                                'interface_name': client_port['interface_name'],
                                'wan_network': service['wan_network'],
                                'uplink_port' : client_node['uplink_port']
                              }

  return parameters



def an_parameters(client, service):
  access_port = get_access_port(service['access_port_id'])
  access_node = get_access_node(service['access_node_id'])

  parameters = { 'provider_vlan': access_node['provider_vlan'],
                 'an_client_port': access_port['port'],
                 'mgmt_ip': access_node['mgmt_ip'],
                 'model': access_node['model'],
                 'vendor': access_node['vendor'] }

  return parameters

