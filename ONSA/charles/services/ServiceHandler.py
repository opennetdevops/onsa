from django.conf import settings
from pprint import pprint
import requests
import json
from charles.views.service import *

def configure_service(config):
	url = settings.WORKER_URL + "services"
	rheaders = {'Content-Type': 'application/json'}
	data = config
	response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

def get_ipam_authentication_token():
	url = "/api/authenticate"
	rheaders = {'Content-Type': 'application/json'}
	#App User
	data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
	response = requests.post(settings.IPAM_URL + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	return json.loads(response.text)['auth_token']


def get_ip_wan_nsx(location,client_name,service_id):
	description = client_name + "-" + service_id
	#"Searchin by owner prefix=WAN_NSX"
	owner = "WAN_NSX_" + location
	token = get_ipam_authentication_token()
	url = settings.IPAM_URL + "/api/networks/assign_ip"
	rheaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
	data = { "description" : description, "owner" : owner,"ip_version" : 4 }
	response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if "network" in json_response:
		return json_response["network"]
	else:
		return None

def get_wan_mpls_network(location,client_name,service_id):
	#Default prefix set by IDR
	mask = 30
	description = client_name + "-" + service_id
	owner = "WAN_MPLS_" + location
	token = get_ipam_authentication_token()
	url = settings.IPAM_URL + "/api/networks/assign_subnet"
	rheaders = {'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + token}
	data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
	response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if "network" in json_response:
		return json_response["network"]
	else:
		return None

def get_client_network(client_name,service_id,mask):
	description = client_name + "-" + service_id
	owner = "PUBLIC_ONSA"
	token = get_ipam_authentication_token()
	url = settings.IPAM_URL + "/api/networks/assign_subnet"
	rheaders = {'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + token}
	data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
	response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if "network" in json_response:
		return json_response["network"]
	else:
		return None

def get_subnets_by_description(description):
	token = get_ipam_authentication_token()
	url = settings.IPAM_URL + "/api/networks?description=" + description
	rheaders = {'Authorization': 'Bearer ' + token}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	return json_response

def release_ip(client_name,product_id):
	description = client_name + "-" + product_id
	subnet = _get_subnets_by_description(description)[0]
	subnet_id = subnet['id']
	token = get_ipam_authentication_token()
	url = settings.IPAM_URL + "/api/networks/" + str(subnet_id) + "/release"
	rheaders = {'Authorization': 'Bearer ' + token}
	response = requests.post(url, auth = None, verify = False, headers = rheaders)

def destroy_subnet(client_name,product_id):
	description = client_name + "-" + product_id
	subnet_to_destroy = _get_subnets_by_description(description)[0]
	subnet_id = subnet['id']
	token = get_ipam_authentication_token()
	url = settings.IPAM_URL + "/api/networks/" + str(subnet_id)
	rheaders = {'Authorization': 'Bearer ' + token}
	response = requests.delete(url, auth = None, verify = False, headers = rheaders)

def get_location(location_id):
	url = settings.INVENTORY_URL + "locations/" + location_id
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def get_router_node(router_node_id):
	url= settings.INVENTORY_URL + "routernodes/"+ router_node_id
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def get_virtual_pod(location_id):
	url= settings.INVENTORY_URL + "locations/"+ location_id + "/virtualpods"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def get_client_node(client_node_sn):
	url= settings.INVENTORY_URL + "clientnodes/"+client_node_sn
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_virtual_pod_downlink_portgroup(virtual_pod_id):
	url= settings.INVENTORY_URL + "virtualpods/"+ virtual_pod_id + "/portgroups?used=false"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def use_portgroup(portgroup_id):
	url= settings.INVENTORY_URL + "portgroups/" + portgroup_id
	rheaders = {'Content-Type': 'application/json'}
	data = {"used":True}
	response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_free_logical_units(router_node_id):
	url = settings.INVENTORY_URL + "routernodes/" + router_node_id + "/logicalunits?used=false"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	#TODO check minimum size = 2
	if json_response:
		return json_response
	else:
		return None

def add_logical_unit_to_router_node(router_node_id,logical_unit_id,product_id):
	url= settings.INVENTORY_URL + "routernodes/" + router_node_id + "/logicalunits"
	rheaders = {'Content-Type': 'application/json'}
	data = {"logical_unit_id":logical_unit_id,
					"product_id":product_id}
	response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_free_access_port(location_id):
	url= settings.INVENTORY_URL + "locations/"+ location_id + "/accessports?used=false"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def use_port(access_port_id):
	url= settings.INVENTORY_URL + "accessports/" + access_port_id
	rheaders = {'Content-Type': 'application/json'}
	data = {"used":True}
	response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_access_node(access_node_id):
	url= settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id)
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_free_vlan_tag(access_port_id):
	url= settings.INVENTORY_URL + "accessnodes/"+ str(access_port_id) + "/vlantags?used=false"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def add_vlan_tag_to_access_node(vlan_tag,access_node_id,access_port_id,service_id,client_node_sn,client_node_port,bandwidth,vrf_id=None):
	url= settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags"
	rheaders = {'Content-Type': 'application/json'}
	data = {"vlan_tag":vlan_tag,
					"service_id":service_id,
					"client_node_sn":client_node_sn,
					"client_node_port":client_node_port,
					"bandwidth":bandwidth,
					"access_port_id":access_port_id,
					"vrf_id": vrf_id}
	response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def update_service(service_id, data):
	url = settings.JEAN_GREY_URL + "services/" + service_id
	rheaders = {'Content-Type': 'application/json'}

	response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_access_node_port(access_port_id):
	url= settings.INVENTORY_URL + "accessports/"+ str(access_port_id)
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_vrf(vrf_name):
	url = settings.INVENTORY_URL + "vrfs?" + "name=" + vrf_name
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def vrf_exists_in_location(vrf_id,location_id):
	url = settings.INVENTORY_URL + "vrfs/" + vrf_id + "/locations/" + str(location_id)
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response["exists"]
	else:
		return None

def add_location_to_vrf(vrf_id,location_id):
	url = settings.INVENTORY_URL + "vrfs/" + vrf_id + "/locations/" + str(location_id)
	rheaders = {'Content-Type': 'application/json'}
	response = requests.put(url, auth = None, verify = False, headers = rheaders)

def generate_cpeless_irs_request(client, service):
	location = get_location(service['location'])
	router_node = get_router_node(services['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])
	client_node = get_client_node(service['client_node_sn'])
	client_port = get_client_port(service['client_port_id'])	

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node['id'])
	logical_unit_id = free_logical_units[0]['logical_unit_id']


	error = False

	if logical_unit_id:
		client_network = get_client_network(client['name'], service['id'], service['prefix'])
		if client_network:
			#Add logicals unit to routernode
			add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])

			service_data = { 'logical_unit_id': logical_unit_id,
							 'public_network': client_network }

			update_service(service['id'], service_data)
			
			config = {
			   "client" : client['name'],
	  		   "service_type" : service['service_type'],
	  		   "service_id" : service['id'],
	  		   "op_type" : "CREATE",
	  		   "parameters" : {
	  		   			"pop_size" : location['pop_size'],       
								"an_uplink_interface" : access_node['uplink_interface'],
								"an_uplink_ports" : access_node['uplink_ports'],
								"logical_unit" : logical_unit_id,   
								"provider_vlan" : access_node['provider_vlan'],      
								"service_vlan" : service['vlan_id'], 
								"client_cidr" : client_network,
								"bandwidth" : service['bandwidth'],
								"an_client_port" : access_port['port'],
								"on_client_port" : client_port['interface_name'],
								"on_uplink_port" : client_node['uplink_port']
							},

			 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
							 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
							 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']}]
			}
			configure_service(config)
		else:
			error = True
	else:
		error = True

	if error:
		service.service_state = ServiceStatuses['ERROR'].value
		service.save()
		print("Not possible service")

def generate_vcpe_irs_request(client, service):
	location = get_location(service['location'])
	router_node = get_router_node(services['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])
	client_node = get_client_node(service['client_node_sn'])
	client_port = get_client_port(service['client_port_id'])		

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node['id'])
	logical_unit_id = free_logical_units[0]['logical_unit_id']
	vcpe_logical_unit_id = free_logical_units[1]['logical_unit_id']
	
	virtual_pod = get_virtual_pod(location['id'])
	downlink_pg = get_virtual_pod_downlink_portgroup(virtual_pod['id'])
	
	error = False

	if len(free_logical_units) >= 2 and downlink_pg:
		wan_ip = get_ip_wan_nsx(location['name'], client['name'], service['id'])
		if wan_ip:
			client_network = get_client_network(client['name'], service['id'], service['prefix'])
			if client_network:
				
				service_data = { 'logical_unit_id': logical_unit_id,
								 'vcpe_logical_unit_id': vcpe_logical_unit_id,
								 'public_network': client_network, 
								 'wan_ip': wan_ip,
								 'portgroup_id': downlink_pg['id'] }

				update_service(service['id'], service_data)

				use_portgroup(downlink_pg['id'])

				add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
				add_logical_unit_to_router_node(router_node['id'], vcpe_logical_unit_id, service['id'])
				config = { 
						  "client" : client['name'],
						  "service_type" : service['service_type'],
						  "service_id" : service['id'],
						  "op_type" : "CREATE",
						  "parameters":{
									"vmw_uplink_interface" : virtual_pod['uplink_interface'],
									"vmw_logical_unit" : vcpe_logical_unit_id,  
									"vmw_vlan" : downlink_pg['vlan_tag'],           
									"an_uplink_interface" : access_node['uplink_interface'],  
									"an_uplink_ports" :   access_node['uplink_ports'],
									"an_logical_unit" : free_logical_units[1]['logical_unit_id'],   
									"provider_vlan" : access_node['provider_vlan'],      
									"service_vlan" : free_vlan_tag['vlan_tag'], 
									"client_cidr" : client_network,
									"wan_ip" : wan_ip,
									"bandwidth" : service['bandwidth'],
									"datacenter_id" : virtual_pod['datacenterId'] ,
									"resgroup_id" : virtual_pod['resourcePoolId'],
									"datastore_id" : virtual_pod['datastoreId'],
									"wan_portgroup_id" : virtual_pod['uplink_pg_id'],
									"lan_portgroup_id" : downlink_pg['dvportgroup_id'],
									"an_client_port" : free_access_port['port'],
									"on_client_port" : client_port['interface_name'],
									"on_uplink_port" : client_node['uplink_port']
								 },
						  "devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
									   {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
									   {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']},
									   {"vendor":virtual_pod['vendor'],"model":virtual_pod['model'],"mgmt_ip":virtual_pod['mgmt_ip']}]
				}
				pprint(config)
				#Call worker
				configure_service(config)
			else:
				#Free wan_ip
				release_ip(client_name,service_id)
				error = True
		else:
			error = True
	else:
		error = True

	if error:
		service.service_state = ServiceStatuses['ERROR'].value
		service.save()
		print("Not possible service")

def generate_cpe_mpls_request(client, service):
	location = get_location(service['location'])
	router_node = get_router_node(services['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])
	client_node = get_client_node(service['client_node_sn'])
	client_port = get_client_port(service['client_port_id'])		
	
	client_as = service['autonomous_system']
	vrf = get_vrf(service['vrf_id'])

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node['id'])
	logical_unit_id = free_logical_units[0]['logical_unit_id']

	vrf_exists = vrf_exists_in_location(vrf['rt'], location['id'])

	error = False

	if logical_unit_id:
		wan_network = get_wan_mpls_network(location['name'], client['name'], service['id'])
		if wan_network: 
			if not vrf_exists:
				add_location_to_vrf(vrf['rt'], location['id'])
			#Add logical unit to router node
			add_logical_unit_to_router_node(router_node['id'], logical_unit_id, service['id'])
			
			service_data = { 'logical_unit_id': logical_unit_id,
							 'client_network': service['client_network'], 
							 'wan_network': wan_network }

			update_service(service_id, service_data)

			config = {
			   "client" : client['name'],
	  		   "service_type" :  service['service_type'],
	  		   "service_id" : service['service_id'],
	  		   "op_type" : "CREATE",
	  		   "parameters" : {
	  		   			"pop_size" : location['pop_size'],       
								"an_uplink_interface" : access_node['uplink_interface'],
								"an_uplink_ports" :   access_node['uplink_ports'],
								"logical_unit" : logical_unit_id,   
								"provider_vlan" : access_node['provider_vlan'],      
								"service_vlan" : service['vlan_id'], 
								"bandwidth" : service['bandwidth'],
								"client_as_number" : client_as,
								"an_client_port" : access_port['port'],
								"on_client_port" : client_port['interface_name'],
								"vrf_exists": vrf_exists,
								"wan_cidr": wan_network,
								"client_cidr": sevice['client_network'],
	            	"vrf_name": vrf['name'],
	            	"vrf_id": vrf['rt'],
	            	"loopback":router_node['loopback']
							},
			 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
							 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
							 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']}]}

			pprint(config)
			#Call worker
			configure_service(config)
		else:
			error = True
	else:
		error = True

	if error:
		service.service_state = ServiceStatuses['ERROR'].value
		service.save()
		print("Not possible service")

def generate_cpeless_mpls_request(client, service):
	location = get_location(service['location'])
	router_node = get_router_node(services['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])
	client_node = get_client_node(service['client_node_sn'])
	client_port = get_client_port(service['client_port_id'])		
	
	client_as = service['autonomous_system']
	vrf = get_vrf(service['vrf_id'])	

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node_id)
	logical_unit_id = free_logical_units[0]['logical_unit_id']

	client_cidr = service['client_network'] + "/" + service['prefix']

	vrf_exists = vrf_exists_in_location(vrf['rt'], location['id'])

	if logical_unit_id:
		service_data = { 'logical_unit_id': logical_unit_id,
						 'client_network': service['client_network'],
						 'autonomous_system': client_as }

		update_service(service['id'], service_data)

		add_logical_unit_to_router_node(router_node['router_node_id'], logical_unit_id, service['id'])
		if not vrf_exists:
			add_location_to_vrf(vrf['rt'], location['id'])

		config = {
		   "client" : client['name'],
  		   "service_type" : service['service_type'],
  		   "service_id" : service['id'],
  		   "op_type" : "CREATE",
  		   "parameters" : {
  		   			"pop_size" : service['pop_size'],       
							"an_uplink_interface" : access_node['uplink_interface'],
							"an_uplink_ports" :   access_node['uplink_ports'],
							"logical_unit" : logical_unit_id,   
							"provider_vlan" : access_node['provider_vlan'],      
							"service_vlan" : free_vlan_tag['vlan_tag'], 
							"bandwidth" : service['bandwidth'],
							"client_cidr" : service['client_network'],
							"an_client_port" : access_port['port'],
							"on_client_port" : client_port['interface_name'],
							"vrf_exists": vrf_exists,
            	"vrf_name": vrf['name'],
            	"vrf_id": vrf['rt'],
            	"loopback":router_node['loopback']
						},
		 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
						 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
						 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']}]}

		pprint(config)
		#Call worker
		configure_service(config)
	else:
		service.service_state = ServiceStatuses['ERROR'].value
		service.save()
		print("Not possible service")

def generate_vpls_request(client, service):
	location = get_location(service['location'])
	router_node = get_router_node(services['router_node_id'])
	access_port = get_access_port(service['access_port_id'])
	access_node = get_access_node(service['access_node_id'])
	client_node = get_client_node(service['client_node_sn'])
	client_port = get_client_port(service['client_port_id'])		
	
	client_as = service['autonomous_system']
	vrf = get_vrf(service['vrf_id'])

	"""
	Fetch for logical units
	"""
	free_logical_units = get_free_logical_units(router_node['id'])
	logical_unit_id = free_logical_units[0]['logical_unit_id']

	
	vrf_exists = vrf_exists_in_location(vrf['rt'],location['id'])

	if 	logical_unit_id:
		service_data = { 'logical_unit_id': logical_unit_id }

		update_service(service['id'], service_data)

		#Add logical unit to router node
		add_logical_unit_to_router_node(router_node_id, free_logical_units[0]['logical_unit_id'], service['id'])
		if not vrf_exists:
			add_location_to_vrf(vrf['rt'], location['id'])

		config = {
		   "client" : client['name'],
  		   "service_type" : service['service_type'],
  		   "service_id" : service['service_id'],
  		   "op_type" : "CREATE",
  		   "parameters" : {
  		   			"pop_size" : service['pop_size'],       
							"an_uplink_interface" : access_node['uplink_interface'],
							"an_uplink_ports" :   access_node['uplink_ports'],
							"logical_unit" : logical_unit_id,   
							"provider_vlan" : access_node['provider_vlan'],      
							"service_vlan" : service['vlan_id'], 
							"bandwidth" : service['bandwidth'],
							"an_client_port" : access_port['port'],
							"on_client_port" : client_port['interface_name'],
							"vrf_exists": vrf_exists,
            	"vrf_name": vrf['name'],
            	"vrf_id": vrf['rt'],
            	"loopback":router_node['loopback']
						},
		 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmt_ip']},
						 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmt_ip']},
						 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmt_ip']}]}

		pprint(config)
		#Call worker
		configure_service(config)
	else:
		service.service_state = ServiceStatuses['ERROR'].value
		service.save()
		print("Not possible service")
