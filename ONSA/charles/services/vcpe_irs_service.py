from charles.utils.utils import *
from charles.views.service import *

from charles.utils.utils import *
from charles.views.service import *

from pprint import pprint

BB_CODES = ["bb", "bb_data"]
CPE_CODES = ["cpe", "cpe_data"]
DATA_CODES = ["bb_data", "cpe_data"]
ACTIVATION_CODES = ["bb", "cpe"]


def generate_vcpe_irs_request(client, service, code=None):

	config = {
		   "client" : client['name'],
		   "service_type" :  service['service_type'],
		   "service_id" : service['id'],
		   "op_type" : "CREATE" }

	if code in BB_CODES:
		parameters = bb_parameters(client, service)
		
		service_data = { 'logical_unit_id': parameters['logical_unit_id'] }

		config['parameters'] =  {
									"pop_size" : parameters['pop_size'],       
									"an_uplink_interface" : parameters['an_uplink_interface'],
									"an_uplink_ports" :   parameters['an_uplink_ports'],
									"logical_unit" : parameters['logical_unit_id'],   
									"provider_vlan" : parameters['provider_vlan'],      
									"service_vlan" : service['vlan_id'], 
									"an_client_port" : parameters['an_client_port'],
									"client_cidr": parameters['client_network'],
									"vmw_uplink_interface" : parameters['virtual_pod']['uplink_interface'],
									"vmw_logical_unit" : parameters['vcpe_logical_unit_id'], 
									"vmw_vlan" : parameters['virtual_pod']['vlan_tag'],
									"wan_ip" : parameters['wan_ip'],
									"datacenter_id" : parameters['virtual_pod']['datacenter_id'] ,
									"resgroup_id" : parameters['virtual_pod']['respool_id'],
									"datastore_id" : parameters['virtual_pod']['datastore_id'],
									"wan_portgroup_id" : parameters['virtual_pod']['wan_portgroup_id'],
									"lan_portgroup_id" : parameters['virtual_pod']['lan_portgroup_id'], 
								}

		config['devices'] = [{"vendor": parameters['router_node']['vendor'],"model": parameters['router_node']['model'],"mgmt_ip": parameters['router_node']['mgmt_ip']},
												 {"vendor": parameters['access_node']['vendor'],"model": parameters['access_node']['model'],"mgmt_ip": parameters['access_node']['mgmt_ip']},
												 {"vendor": parameters['virtual_pod']['vendor'],"model": parameters['virtual_pod']['model'],"mgmt_ip": parameters['virtual_pod']['mgmt_ip']}]

		if code == "bb_data":
			service_data['service_state'] = "BB_DATA_ACK"

		elif code == "bb":
			service_data['service_state'] = "BB_ACTIVATION_IN_PROGRESS"

		update_service(service['id'], service_data)

	elif code in CPE_CODES:
		parameters = cpe_parameters(client, service)

		config['parameters'] =  {  
															"service_vlan" : service['vlan_id'], 
															"bandwidth" : service['bandwidth'],
															"on_client_port" : parameters['client_node']['interface_name'],
															"on_uplink_port" : parameters['client_node']['uplink_port']
														}

		config['devices'] = [{"vendor": parameters['client_node']['vendor'], "model": parameters['client_node']['model'], "mgmt_ip": parameters['client_node']['mgmt_ip']}]


		if code == "cpe_data":
			service_data = { "service_state": "CPE_DATA_ACK" }

		elif code == "cpe":
			service_data = { "service_state": "CPE_ACTIVATION_IN_PROGRESS" }

		update_service(service['id'], service_data) 

	if code in DATA_CODES:
		print("DATA_FECTH")
		return config, service_data['service_state']
	elif code in ACTIVATION_CODES:
		print("ACTIVATION")
		# configure_service(config)
		return config, service_data['service_state']
	else:
		return None, service_state['service_state']


def bb_parameters(client, service):
	location = get_location(service['location_id'])
	router_node = get_router_node(service['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node['id'])
	logical_unit_id = free_logical_units[0]['logical_unit_id']
	vcpe_logical_unit_id = free_logical_units[1]['logical_unit_id']

	virtual_pod = get_virtual_pods(location['id'])[0]
	downlink_pg = get_virtual_pod_downlink_portgroup(virtual_pod['id'])

	if len(free_logical_units) >= 2 and downlink_pg:
		wan_ip = get_ip_wan_nsx(location['name'], client['name'], service['id'])
		if wan_ip:
			client_network = get_client_network(client['name'], service['id'], service['prefix'])
			if client_network:
				add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
				add_logical_unit_to_router_node(router_node['id'], vcpe_logical_unit_id, service['id'])
		else:
			return None
	else:
		return None

	parameters = {
				   'pop_size': location['pop_size'],
				   'an_uplink_interface' : access_node['uplink_interface'],
				   'an_uplink_ports' :   access_node['uplink_ports'],
				   'logical_unit_id': logical_unit_id,
				   'vcpe_logical_unit_id': vcpe_logical_unit_id,   
				   'provider_vlan' : access_node['provider_vlan'],      
				   'an_client_port' : access_port['port'],
				   'wan_ip': wan_ip,
				   'client_network': client_network,
				   'virtual_pod': {
									'uplink_interface' : virtual_pod['uplink_interface'],
									'vcpe_logical_unit' : vcpe_logical_unit_id, 
									'vlan_tag' : downlink_pg['vlan_tag'],
									'datacenter_id' : virtual_pod['datacenter_id'] ,
									'respool_id' : virtual_pod['respool_id'],
									'datastore_id' : virtual_pod['datastore_id'],
									'wan_portgroup_id' :virtual_pod['uplink_pg_id'],
									'lan_portgroup_id' : downlink_pg['id'], 

				   }                                    
				}
			
	parameters['router_node'] = { 'vendor': router_node['vendor'],
															  'model': router_node['model'],
															  'mgmt_ip': router_node['mgmt_ip']
															}
	parameters['access_node'] = { 'vendor': access_node['vendor'],
															  'model': access_node['model'],
															  'mgmt_ip': access_node['mgmt_ip']
															}
	parameters['virtual_pod'].update({ 'vendor': virtual_pod['vendor'],
															  'model': virtual_pod['model'],
															  'mgmt_ip': virtual_pod['mgmt_ip']
															})

	return parameters

def cpe_parameters(client, service):
	location = get_location(service['location_id'])
	client_node = get_client_node(service['client_node_sn'])
	client_port = get_client_port(service['client_node_sn'], service['client_port_id'])

	parameters = { 'client_node': {
																	'vendor': client_node['vendor'],
																  'model': client_node['model'],
																  'mgmt_ip': client_node['mgmt_ip'],
																  'interface_name': client_port['interface_name'],
																  'uplink_port' : client_node['uplink_port']
																  
																} }

	return parameters