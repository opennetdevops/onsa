# Python imports
import logging
from pprint import pprint

# ONSA imports
from charles.utils.utils import *
from charles.utils.inventory_utils import *
from charles.utils.ipam_utils import *
from charles.constants import *
from charles.models import *


# Naming convention for functions inside this class
# "service_state" + "_" + deployment_mode + "_request"


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
    
    logging.debug(f'releasing service resources, accessport')
    logging.debug(service['access_port_id'])
    release_access_port(service['access_port_id'])
    logging.debug(f'releasing service resources, vlanId')
    logging.debug(service['vlan_id'])
    logging.debug(service['access_node_id'])
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

  service_data['service_state'] = service_state
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



def bb_data_ack_automated_request(service):
  # if DEBUG: print("bb_data_ack_automated_request")
  # client = get_client(service['client_id'])
  # parameters = bb_parameters(client, service)

  # if DEBUG: print(parameters)

  # #Handle parameters error
  # if parameters is not None:
  # 	service_data = { 'logical_unit_id': parameters['logical_unit_id'],
  # 					 'wan_network':  parameters['wan_network'],
  # 					 'autonomous_system':  parameters['client_as_number'],
  # 					 'vrf_id': parameters['vrf_id'] }

  # 	service_data['client_network'] = service['client_network']
  # 	service_data['service_state'] = "bb_data_ack"
  # 	update_jeangrey_service(service['service_id'], service_data)

  # else:
  # 	service_data['service_state'] = "error"
  # 	update_jeangrey_service(service['service_id'], service_data)
  # return service_data['service_state']
  pass


def bb_activated_automated_request(service):
  # if DEBUG: print("bb_activated_automated_request")
  # client = get_client(service['client_id'])
  # parameters = bb_parameters(client, service)

  # config = {
  # 		 "client" : client['name'],
  # 		 "service_type" :  service['service_type'],
  # 		 "service_id" : service['service_id'],
  # 		 "op_type" : "CREATE" }

  # config['parameters'] =  {
  # 						"pop_size" : parameters['pop_size'],
  # 						"an_uplink_interface" : parameters['an_uplink_interface'],
  # 						"an_uplink_ports" :   parameters['an_uplink_ports'],
  # 						"logical_unit" : parameters['logical_unit_id'],
  # 						"provider_vlan" : parameters['provider_vlan'],
  # 						"service_vlan" : service['vlan_id'],
  # 						"client_as_number" : parameters['client_as_number'],
  # 						"an_client_port" : parameters['an_client_port'],
  # 						"vrf_exists": parameters['vrf_exists'],
  # 						"wan_cidr": parameters['wan_network'],
  # 						"client_cidr": service['client_network'],
  # 						"vrf_name": parameters['vrf_name'],
  # 						"vrf_id": parameters['vrf_id'],
  # 						"loopback":parameters['loopback']
  # 					}

  # config['devices'] = [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']}]

  # configure_service(config)
  # service_data = {}
  # service_data['service_state'] = "bb_activation_in_progress"
  # update_jeangrey_service(service['service_id'], service_data)
  # return service_data['service_state']
  pass


def an_data_ack_automated_request(service):
  # if DEBUG: print("an_data_ack_automated_request")
  # service_data = {}
  # service_data['service_state'] = "an_data_ack"
  # update_jeangrey_service(service['service_id'], service_data)
  # return service_data['service_state']
  pass






def cpe_data_ack_automated_request(service):
  # if DEBUG: print("cpe_data_ack_automated_request")
  # client = get_client(service['client_id'])
  # parameters = cpe_parameters(client, service)
  # customer_location = get_customer_location(service['client_id'], service['customer_location_id'])

  # if parameters['client_port_id']:
  # 	service_data = { "client_port_id": parameters['client_port_id'] }

  # service_data['service_state'] = "cpe_data_ack"
  # service_data['wan_network'] = service['wan_network'] 	

  # update_jeangrey_service(service['service_id'], service_data)
  # return service_data['service_state']
  pass


def service_activated_automated_request(service):
  # if DEBUG: print("service_activated_automated_request")
  # client = get_client(service['client_id'])
  # parameters = cpe_parameters(client, service)
  # config = {
  # 	 "client" : client['name'],
  # 	 "service_type" :  service['service_type'],
  # 	 "service_id" : service['service_id'],
  # 	 "op_type" : "CREATE" }


  # service_data = {}

  # if parameters is not None:
  # 	config['parameters'] =  {  
  # 							"service_vlan" : service['vlan_id'], 
  # 							"bandwidth" : service['bandwidth'],
  # 							"client_as_number" : service['autonomous_system'],
  # 							"on_client_port" : parameters['client_node']['interface_name'],
  # 							"wan_cidr": service['wan_network'],
  # 							"client_cidr": service['client_network'],
  # 						 }

  # 	config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


  # 	service_data['service_state'] = "cpe_activation_in_progress"
  # 	configure_service(config)
  # else:
  # 	service_data['service_state'] = "error"
  
  # update_jeangrey_service(service['service_id'], service_data)
  # return service_data['service_state']
  pass



def bb_parameters(client, service):
  pass
  # location = get_location(service['location_id'])
  # router_node = get_router_node(service['router_node_id'])
  # access_port = get_access_port(service['access_port_id'])
  # access_node = get_access_node(service['access_node_id'])

  # #vrf = get_vrf(service['vrf_id'])

  # #Asignar vrf y AS 
  # data = define_vrf(client, service)

  # """
  # Fetch for logical units
  # """
  # free_logical_units = get_free_logical_units(router_node['id'])
  # logical_unit_id = free_logical_units[0]['logical_unit_id']

  # vrf_exists = vrf_exists_in_location(data['vrf_id'], location['id'])

  # parameters = { 'pop_size': location['pop_size'],
  # 				 'an_uplink_interface' : access_node['uplink_interface'],
  # 				 'an_uplink_ports' :   access_node['uplink_ports'],
  # 				 'logical_unit_id': logical_unit_id,   
  # 				 'provider_vlan' : access_node['provider_vlan'],      
  # 				 'an_client_port' : access_port['port'],
  # 				 'vrf_exists': vrf_exists,
  # 				 'vrf_name': data['vrf_name'],
  # 				 'vrf_id': data['vrf_id'],
  # 				 'loopback': router_node['loopback']}

  # if logical_unit_id:
  # 	wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])
  # 	if wan_network: 
  # 		if not vrf_exists:
  # 			vrf = {"vrf_id":data['vrf_id']}
  # 			add_vrf_to_location(location['id'],vrf)
  # 		#Add logical unit to router node
  # 		add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
      
  # 		client_as_number = data['autonomous_system']

  # 		parameters['wan_network'] = wan_network
  # 		parameters['client_as_number'] = client_as_number

  # parameters['router_node'] = { 'vendor': router_node['vendor'],
  # 								'model': router_node['model'],
  # 								'mgmt_ip': router_node['mgmt_ip']
  # 							}
  # parameters['access_node'] = { 'vendor': access_node['vendor'],
  # 								'model': access_node['model'],
  # 								'mgmt_ip': access_node['mgmt_ip']
  # 							}

  # # pprint(parameters)

  # return parameters

def cpe_parameters(client, service):
  pass
  # location = get_location(service['location_id'])
  # client_node = get_client_node(service['client_node_sn'])
  # parameters = {}
  
  # if service['client_port_id'] is None:
  # 	customer_location = get_customer_location(client['id'],service['customer_location_id']) 
  # 	client_port_id = fetch_cpe(service['client_node_sn'], client['name'], customer_location )
  # 	client_port = get_client_port(service['client_node_sn'], client_port_id)
  # 	parameters['client_port_id'] = client_port_id

  # else:
  # 	client_port = get_client_port(service['client_node_sn'], service['client_port_id'])
  
  # wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])

  
  # parameters['client_node'] = { 'vendor': client_node['vendor'],
  # 								'model': client_node['model'],
  # 								'mgmt_ip': client_node['mgmt_ip'],
  # 								'interface_name': client_port['interface_name'],
  # 								'wan_network': wan_network }

  # return parameters

def define_vrf(client, service):
  pass
    # if service['vrf_id'] is None:
    #     vrf_list = get_client_vrfs(client['name'])

    #     vrf_name = "VPLS-" + client['name'] if service['service_type'] in VPLS_SERVICES else "VRF-" + client['name']    
    #     vrf_name += "-" + str(len(vrf_list)+1) if vrf_list is not None else "-1"
        
    #     vrf = get_free_vrf()
    #     if vrf is not None:
    #         service['vrf_id'] = vrf['rt']
    #         use_vrf(service['vrf_id'], vrf_name, client['name'])
    #         service['vrf_name'] = vrf_name
    #     else:
    #         print("ERROR NON VRF AVAILABLE")
    # else:
    #   service['vrf_name'] = get_vrf(service['vrf_id'])['name']
    
    # service['autonomous_system'] = assign_autonomous_system(service['vrf_id'])

    # return service
