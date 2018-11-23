from charles.utils.utils import *
# from charles.views.service import *

from pprint import pprint

BB_CODES = ["bb", "bb_data"]
CPE_CODES = ["cpe", "cpe_data"]
DATA_CODES = ["bb_data", "cpe_data"]
ACTIVATION_CODES = ["bb", "cpe"]
DEBUG = True


# Naming convention for functions inside this class
# "service_state" + "_" + deployment_mode + "_request"

def bb_data_ack_automated_request(service):
	if DEBUG: print("bb_data_ack_automated_request")
	client = get_client(service['client_id'])
	parameters = bb_parameters(client, service)

	if DEBUG: print(parameters)

	#Handle parameters error
	if parameters is not None:
		service_data = { 'logical_unit_id': parameters['logical_unit_id'],
						 'wan_network':  parameters['wan_network'],
						 'autonomous_system':  parameters['client_as_number'] }

		service_data['client_network'] = service['client_network']
		service_data['service_state'] = "bb_data_ack"
		update_service(service['service_id'], service_data)

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
							"client_as_number" : parameters['client_as_number'],
							"an_client_port" : parameters['an_client_port'],
							"vrf_exists": parameters['vrf_exists'],
							"wan_cidr": parameters['wan_network'],
							"client_cidr": service['client_network'],
							"vrf_name": parameters['vrf_name'],
							"vrf_id": parameters['vrf_id'],
							"loopback":parameters['loopback']
						}

	config['devices'] = [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']},
						 {"vendor": parameters['access_node']['vendor'],"model": parameters['access_node']['model'],"mgmt_ip": parameters['access_node']['mgmt_ip']}]

	configure_service(config)
	service_data = {}
	service_data['service_state'] = "BB_ACTIVATION_IN_PROGRESS"
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
		service_data['service_state'] = "AN_ACTIVATION_IN_PROGRESS"
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
		service_data = { "client_port_id": parameters['client_port_id'] }

	service_data['service_state'] = "cpe_data_ack"
	service_data['wan_network'] = parameters['client_node']['wan_network'] 	

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
								"client_as_number" : service['autonomous_system'],
								"on_client_port" : parameters['client_node']['interface_name'],
								"wan_cidr": service['wan_network'],
								"client_cidr": service['client_network'],
							 }

		config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


		service_data['service_state'] = "CPE_ACTIVATION_IN_PROGRESS"
		configure_service(config)
	else:
		service_data['service_state'] = "error"
	
	update_service(service['service_id'], service_data)
	return service_data['service_state']




# def generate_cpe_mpls_automated_request(client, service, code=None):

# 	config = {
# 				 "client" : client['name'],
# 				 "service_type" :  service['service_type'],
# 				 "service_id" : service['id'],
# 				 "op_type" : "CREATE" }
	
# 	if code in BB_CODES:
# 		parameters = bb_parameters(client, service)
		
# 		service_data = { 'logical_unit_id': parameters['logical_unit_id'],
# 						 'wan_network':  parameters['wan_network'],
# 						 'autonomous_system':  parameters['client_as_number'] }

# 		service_data['client_network'] = service['client_network']

# 		config['parameters'] =  {
# 								"pop_size" : parameters['pop_size'],       
# 								"an_uplink_interface" : parameters['an_uplink_interface'],
# 								"an_uplink_ports" :   parameters['an_uplink_ports'],
# 								"logical_unit" : parameters['logical_unit_id'],   
# 								"provider_vlan" : parameters['provider_vlan'],      
# 								"service_vlan" : service['vlan_id'], 
# 								"client_as_number" : parameters['client_as_number'],
# 								"an_client_port" : parameters['an_client_port'],
# 								"vrf_exists": parameters['vrf_exists'],
# 								"wan_cidr": parameters['wan_network'],
# 								"client_cidr": service['client_network'],
# 								"vrf_name": parameters['vrf_name'],
# 								"vrf_id": parameters['vrf_id'],
# 								"loopback":parameters['loopback']
# 							}

# 		config['devices'] = [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']},
# 							 {"vendor": parameters['access_node']['vendor'],"model": parameters['access_node']['model'],"mgmt_ip": parameters['access_node']['mgmt_ip']}]


# 		if code == "bb_data":
# 			service_data['service_state'] = "BB_DATA_ACK"

# 		elif code == "bb":
# 			service_data['service_state'] = "BB_ACTIVATION_IN_PROGRESS"

# 		update_service(service['id'], service_data) 
# #
# 	elif code in CPE_CODES:
# 		parameters = cpe_parameters(client, service)

# 		config['parameters'] =  {  
# 								"service_vlan" : service['vlan_id'], 
# 								"bandwidth" : service['bandwidth'],
# 								"client_as_number" : service['autonomous_system'],
# 								"on_client_port" : parameters['client_node']['interface_name'],
# 								"wan_cidr": service['wan_network'],
# 								"client_cidr": service['client_network'],
# 							 }

# 		config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


# 		if code == "cpe_data":
# 			service_data = { "service_state": "CPE_DATA_ACK", "wan_network": parameters['client_node']['wan_network'] }

# 		elif code == "cpe":
# 			service_data = { "service_state": "CPE_ACTIVATION_IN_PROGRESS" , "wan_network": parameters['client_node']['wan_network'] }

# 		update_service(service['id'], service_data)

# 	elif code == "an":
# 		parameters = an_parameters(client, service)

# 		config['parameters'] =  {  
# 								"service_vlan" : service['vlan_id'], 
# 								"an_client_port": parameters['an_client_port']
# 									}

# 		config['devices'] = [{"vendor": parameters['vendor'], "model": parameters['model'], "mgmt_ip": parameters['mgmt_ip']}]


# 		service_data = { "service_state": "AN_ACTIVATED" }

# 		update_service(service['id'], service_data)
			
# 	if code in DATA_CODES:
# 		print("DATA_FECTH")
# 		return config, service_data['service_state']
# 	elif code in ACTIVATION_CODES:
# 		print("ACTIVATION")
# 		# configure_service(config)
# 		return config, service_data['service_state']
# 	elif code == "an":
# 		print("AN ACTIVATION")
# 		# configure_service(config)
# 		return config, service_data['service_state']
# 	else:
# 		return None, service_state['service_state']
 

def bb_parameters(client, service):
	location = get_location(service['location_id'])
	router_node = get_router_node(service['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])

	vrf = get_vrf(service['vrf_id'])

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node['id'])
	logical_unit_id = free_logical_units[0]['logical_unit_id']

	vrf_exists = vrf_exists_in_location(vrf['rt'], location['id'])

	parameters = { 'pop_size': location['pop_size'],
					 'an_uplink_interface' : access_node['uplink_interface'],
					 'an_uplink_ports' :   access_node['uplink_ports'],
					 'logical_unit_id': logical_unit_id,   
					 'provider_vlan' : access_node['provider_vlan'],      
					 'an_client_port' : access_port['port'],
					 'vrf_exists': vrf_exists,
					 'vrf_name': vrf['name'],
					 'vrf_id': vrf['rt'],
					 'loopback': router_node['loopback']}

	if logical_unit_id:
		wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])
		if wan_network: 
			if not vrf_exists:
				add_location_to_vrf(vrf['rt'], location['id'])
			#Add logical unit to router node
			add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
			
			client_as_number = service['autonomous_system']

			parameters['wan_network'] = wan_network
			parameters['client_as_number'] = client_as_number

	parameters['router_node'] = { 'vendor': router_node['vendor'],
									'model': router_node['model'],
									'mgmt_ip': router_node['mgmt_ip']
								}
	parameters['access_node'] = { 'vendor': access_node['vendor'],
									'model': access_node['model'],
									'mgmt_ip': access_node['mgmt_ip']
								}

	# pprint(parameters)

	return parameters

def cpe_parameters(client, service):
	location = get_location(service['location_id'])
	client_node = get_client_node(service['client_node_sn'])
	parameters = {}
	
	if service['client_port_id'] is None:
		customer_location = get_customer_location(client['id'],service['customer_location_id']) 
		client_port_id = fetch_cpe(service['client_node_sn'], client['name'], customer_location )
		client_port = get_client_port(service['client_node_sn'], client_port_id)
		parameters['client_port_id'] = client_port_id

	else:
		client_port = get_client_port(service['client_node_sn'], service['client_port_id'])
	
	wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])

	
	parameters['client_node'] = { 'vendor': client_node['vendor'],
									'model': client_node['model'],
									'mgmt_ip': client_node['mgmt_ip'],
									'interface_name': client_port['interface_name'],
									'wan_network': wan_network }

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