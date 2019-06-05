# Python imports
import logging
from pprint import pprint

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
    logging.debug("deleting service")
    
    #Send message(job) to Queue so workers can take it
    configure_service(config) 
  except BaseException:
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


# def generate_cpeless_mpls_request(client, service, code=None):

# 		config = {
# 								 "client" : client['name'],
# 								 "service_type" :  service['service_type'],
# 								 "service_id" : service['id'],
# 								 "op_type" : "CREATE" }
		
# 		if code in BB_CODES:
# 				parameters = bb_parameters(client, service)
				
# 				service_data = { 'logical_unit_id': parameters['logical_unit_id'], 'client_network': service['client_network'] }

# 				config['parameters'] =  {
# 																"pop_size" : parameters['pop_size'],       
# 																"an_uplink_interface" : parameters['an_uplink_interface'],
# 																"an_uplink_ports" :   parameters['an_uplink_ports'],
# 																"logical_unit" : parameters['logical_unit_id'],   
# 																"provider_vlan" : parameters['provider_vlan'],      
# 																"service_vlan" : service['vlan_id'], 
# 																"an_client_port" : parameters['an_client_port'],
# 																"vrf_exists": parameters['vrf_exists'],
# 																"client_cidr": service['client_network'],
# 																"vrf_name": parameters['vrf_name'],
# 																"vrf_id": parameters['vrf_id'],
# 																"loopback":parameters['loopback']
# 														}

# 				config['devices'] = [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']},
# 														 {"vendor": parameters['access_node']['vendor'],"model": parameters['access_node']['model'],"mgmt_ip": parameters['access_node']['mgmt_ip']}]


# 				if code == "bb_data":
# 						service_data['service_state'] = "BB_DATA_ACK"

# 				elif code == "bb":
# 						service_data['service_state'] = "bb_activation_in_progress"

# 				update_jeangrey_service(service['id'], service_data) 

# 		elif code in CPE_CODES:
# 				parameters = cpe_parameters(client, service)

# 				config['parameters'] =  {  
# 											"service_vlan": service['vlan_id'], 
# 											"bandwidth": service['bandwidth'],
# 											"client_as_number": service['autonomous_system'],
# 											"on_client_port": parameters['client_node']['interface_name'],
# 											"on_uplink_port": parameters['client_node']['uplink_port'],
# 											"client_cidr": service['client_network']
# 										}

# 				config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


# 				if code == "cpe_data":
# 						service_data = { "service_state": "CPE_DATA_ACK" }

# 				elif code == "cpe":
# 						service_data = { "service_state": "cpe_activation_in_progress" }

# 				update_jeangrey_service(service['id'], service_data)
						
# 		if code in DATA_CODES:
# 				print("DATA_FECTH")
# 				return config, service_data['service_state']
# 		elif code in ACTIVATION_CODES:
# 				print("ACTIVATION")
# 				# configure_service(config)
# 				return config, service_data['service_state']
# 		else:
# 				return None, service_state['service_state']
 



def bb_data_ack_automated_request(service):
	pass



def bb_activated_automated_request(service):
	pass


def an_data_ack_automated_request(service):
	pass


def cpe_data_ack_automated_request(service):
	pass


def service_activated_automated_request(service):
	pass


def bb_parameters(client, service):
	pass
	# location = get_location(service['location_id'])
	# router_node = get_router_node(service['router_node_id'])
	# access_port = get_access_port(service['access_port_id'])
	# access_node = get_access_node(service['access_node_id'])

	# vrf = get_vrf(service['vrf_id'])

	# """
	# Fetch for logical units
	# """
	# free_logical_units = get_free_logical_units(router_node['id'])
	# logical_unit_id = free_logical_units[0]['logical_unit_id']

	# vrf_exists = vrf_exists_in_location(vrf['rt'], location['id'])

	# parameters = { 'pop_size': location['pop_size'],
	# 			 'an_uplink_interface' : access_node['uplink_interface'],
	# 			 'an_uplink_ports' :   access_node['uplink_ports'],
	# 			 'logical_unit_id': logical_unit_id,   
	# 			 'provider_vlan' : access_node['provider_vlan'],      
	# 			 'an_client_port' : access_port['port'],
	# 			 'vrf_exists': vrf_exists,
	# 			 'vrf_name': vrf['name'],
	# 			 'vrf_id': vrf['rt'],
	# 			 'loopback': router_node['loopback'] }

	# if logical_unit_id:
	# 		if not vrf_exists:
	# 			vrf = {"vrf_id":data['vrf_id']}
	# 			add_vrf_to_location(location['id'],vrf)					
	# 			#Add logical unit to router node
	# 		add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
					
	# 		client_as_number = service['autonomous_system']

	# parameters['router_node'] = { 'vendor': router_node['vendor'],
	# 																'model': router_node['model'],
	# 																'mgmt_ip': router_node['mgmt_ip']
	# 														}
	# parameters['access_node'] = { 'vendor': access_node['vendor'],
	# 																'model': access_node['model'],
	# 																'mgmt_ip': access_node['mgmt_ip']
	# 														}

	# # pprint(parameters)

	# return parameters

def cpe_parameters(client, service):
	pass
	# location = get_location(service['location_id'])
	# client_node = get_client_node(service['client_node_sn'])
	# client_port = get_client_port(service['client_node_sn'], service['client_port_id'])

	# wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])

	# parameters = { 'client_node': {
	# 																'vendor': client_node['vendor'],
	# 																'model': client_node['model'],
	# 																'mgmt_ip': client_node['mgmt_ip'],
	# 																'interface_name': client_port['interface_name'],
	# 																'uplink_port' : client_node['uplink_port']}
	# 						}

	# return parameters
