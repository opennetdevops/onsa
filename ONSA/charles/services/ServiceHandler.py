from pprint import pprint
import requests
import json
from ..views.service import *

IPAM_BASE = "http://10.120.78.90"
BASE = "http://localhost:8000"

class ServiceHandler():

	def _configure_service(config):
		url = "/worker/api/services"
		rheaders = {'Content-Type': 'application/json'}
		data = config
		response = requests.post(BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

	def _get_ipam_authentication_token():
		url = "/api/authenticate"
		rheaders = {'Content-Type': 'application/json'}
		#App User
		data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
		response = requests.post(IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)['auth_token']


	def _get_ip_wan_nsx(location,client_name,service_id):
		description = client_name + "-" + service_id
		#"Searchin by owner prefix=WAN_NSX"
		owner = "WAN_NSX_" + location
		token = ServiceHandler._get_ipam_authentication_token()
		url = "/api/networks/assign_ip"
		rheaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
		data = { "description" : description, "owner" : owner,"ip_version" : 4 }
		response = requests.post(IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if "network" in json_response:
			return json_response["network"]
		else:
			return None

	def _get_client_network(client_name,service_id,mask):
		description = client_name + "-" + service_id
		owner = "PUBLIC_ONSA"
		token = ServiceHandler._get_ipam_authentication_token()
		url = "/api/networks/assign_subnet"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
		response = requests.post(IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if "network" in json_response:
			return json_response["network"]
		else:
			return None

	def _get_location(location_name):
		url= "/inventory/api/locations?name="+location_name
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_router_node(location_id):
		url= "/inventory/api/locations/"+ location_id + "/routernodes"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_virtual_pod(location_id):
		url= "/inventory/api/locations/"+ location_id + "/virtualpods"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_client_node(client_node_sn):
		url= "/inventory/api/clientnodes/"+client_node_sn
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_virtual_pod_downlink_portgroup(virtual_pod_id):
		url= "/inventory/api/virtualpods/"+ virtual_pod_id + "/portgroups?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _use_portgroup(portgroup_id):
		url= "/inventory/api/portgroups/" + portgroup_id
		rheaders = {'Content-Type': 'application/json'}
		data = {"used":True}
		response = requests.put(BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_free_logical_units(router_node_id):
		url= "/inventory/api/routernodes/" + router_node_id + "/logicalunits?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		#TODO check minimum size = 2
		if json_response:
			return json_response
		else:
			return None

	def _add_logical_unit_to_router_node(router_node_id,logical_unit_id):
		url= "/inventory/api/routernodes/" + router_node_id + "/logicalunits"
		rheaders = {'Content-Type': 'application/json'}
		data = {"logical_unit_id":logical_unit_id}
		response = requests.post(BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_free_access_port(location_id):
		url= "/inventory/api/locations/"+ location_id + "/accessports?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _use_port(access_port_id):
		url= "/inventory/api/accessports/" + access_port_id
		rheaders = {'Content-Type': 'application/json'}
		data = {"used":True}
		response = requests.put(BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_access_node(access_node_id):
		url= "/inventory/api/accessnodes/"+ access_node_id 
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_free_vlan_tag(access_port_id):
		url= "/inventory/api/accessnodes/"+ access_port_id + "/vlantags?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _add_vlan_tag_to_access_node(vlan_tag,access_node_id,access_port_id,service_id,client_node_sn,client_node_port,bandwidth):
		url= "/inventory/api/accessnodes/"+ access_node_id + "/vlantags"
		rheaders = {'Content-Type': 'application/json'}
		data = {"vlan_tag":vlan_tag,
						"service_id":service_id,
						"client_node_sn":client_node_sn,
						"client_node_port":client_node_port,
						"bandwidth":bandwidth,
						"access_port_id":access_port_id}
		response = requests.post(BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_access_node_port(access_port_id):
		url= "/inventory/api/accessports/"+ access_port_id 
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_vrf(vrf_name):
		url = "/inventory/api/vrfs?" + "name=" + vrf_name
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _vrf_exists_in_location(vrf_id,location_id):
		url = "/api/vrfs/" + vrf_id + "/locations/" + location_id
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response["exists"]
		else:
			return None

	#Generate Services methods
	def generate_cpeless_irs_request(params):
		client_name = params['data_model']['client_name']
		location_name = params['data_model']['location']
		service_id = params['data_model']['service_id']
		service_type = params['data_model']['service_type']

		prefix = params['prefix']
		bandwidth  = params['bandwidth']
		client_node_sn = params['client_node_sn']
		client_node_port = params['client_node_port']

		client_network = ServiceHandler._get_client_network(client_name,service_id,prefix)
		location = ServiceHandler._get_location(location_name)
		location_id = str(location['id'])
		pop_size = location['pop_size']
		router_node = ServiceHandler._get_router_node(location_id)
		router_node_id = str(router_node['id'])
		free_logical_units = ServiceHandler._get_free_logical_units(router_node_id)

		#Add logicals unit to routernode
		ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'])

		# free_access_port = ServiceHandler._get_free_access_port(location_id)
		access_port_id = params['access_port_id']
		access_node_id = params['access_node_id']

		#Mark access port as used
		# ServiceHandler._use_port(access_port_id)
		# access_node_id = str(free_access_port['accessNode_id'])
		access_node = ServiceHandler._get_access_node(access_node_id)
		free_vlan_tag = ServiceHandler._get_free_vlan_tag(access_node_id)
		free_access_port = ServiceHandler._get_access_node_port(access_port_id)

		#Add vlan tag to access port, serviceid,bandwidth, device SN
		ServiceHandler._add_vlan_tag_to_access_node(free_vlan_tag['vlan_tag'],
												access_node_id,
												access_port_id,
												service_id,
												client_node_sn,
												client_node_port,
												bandwidth)

		#Get client node by SN
		client_node = ServiceHandler._get_client_node(client_node_sn)
		# print("CN:",client_node)

		config = {
				   "client" : client_name,
		  		   "service_type" : service_type,
		  		   "service_id" : service_id,
		  		   "op_type" : "CREATE",
		  		   "parameters" : {
		  		   			"pop_size" : pop_size,       
									"an_uplink_interface" : access_node['uplinkInterface'],
									"an_uplink_ports" :   access_node['uplink_ports'],
									"an_logical_unit" : free_logical_units[0]['logical_unit_id'],   
									"provider_vlan" : access_node['qinqOuterVlan'],      
									"service_vlan" : free_vlan_tag['vlan_tag'], 
									"public_cidr" : client_network,
									"bandwidth" : bandwidth,
									"an_client_port" : free_access_port['port'],
									"on_client_port" : client_node_port,
									"on_uplink_port" : client_node['uplink_port']
								},

				 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP']},
								 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
								 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]
				}

		#TODO: check if API returns empty values and do rollback
		if client_network:
			pprint(config)
			#Call worker
			ServiceHandler._configure_service(config)
		else:
			service.service_state = ServiceStatuses['ERROR'].value
			service.save()
			print("Not possible service")

	def generate_vcpe_irs_request(params):		

		client_name = params['data_model']['client_name']
		location_name = params['data_model']['location']
		service_id = params['data_model']['service_id']
		service_type = params['data_model']['service_type']

		prefix = params['prefix']
		bandwidth  = params['bandwidth']
		client_node_sn = params['client_node_sn']
		client_node_port = params['client_node_port']
		access_port_id = params['access_port_id']
		access_node_id = params['access_node_id']

		ip_wan = ServiceHandler._get_ip_wan_nsx(location, client_name, service_id)
		client_network = ServiceHandler._get_client_network(client_name, service_id, prefix)
		location = ServiceHandler._get_location(location_name)
		location_id = str(location['id'])
		virtual_pod = ServiceHandler._get_virtual_pod(location_id)
		router_node = ServiceHandler._get_router_node(location_id)
		downlink_pg = ServiceHandler._get_virtual_pod_downlink_portgroup(str(virtual_pod['id']))

		free_access_port = ServiceHandler._get_access_node_port(access_port_id)

		#Use porgroup
		portgroup_id = str(downlink_pg['id'])
		ServiceHandler._use_portgroup(portgroup_id)

		router_node_id = str(router_node['id'])
		free_logical_units = ServiceHandler._get_free_logical_units(router_node_id)

		#Add logicals unit to routernode
		ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'])
		ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[1]['logical_unit_id'])

		#Mark access port as used
		# ServiceHandler._use_port(access_port_id)
		# access_node_id = str(free_access_port['accessNode_id'])
		# access_node = ServiceHandler._get_access_node(access_node_id)
		free_vlan_tag = ServiceHandler._get_free_vlan_tag(access_node_id)

		#Add vlan tag to access port, serviceid,bandwidth, device SN
		ServiceHandler._add_vlan_tag_to_access_node(free_vlan_tag['vlan_tag'],
													access_node_id,
													access_port_id,
													service_id,
													client_node_sn,
													client_node_port,
													bandwidth)

		#Get client node by SN
		client_node = ServiceHandler._get_client_node(client_node_sn)

		config = { 
				  "client" : client_name,
				  "service_type" : service_type,
				  "service_id" : service_id,
				  "op_type" : "CREATE",
				  "parameters":{
							"vmw_uplink_interface" : virtual_pod['uplinkInterface'],
							"vmw_logical_unit" : free_logical_units[0]['logical_unit_id'],  
							"vmw_vlan" : downlink_pg['vlan_tag'],           
							"an_uplink_interface" : access_node['uplinkInterface'],  
							"an_uplink_ports" :   access_node['uplink_ports'],
							"an_logical_unit" : free_logical_units[1]['logical_unit_id'],   
							"provider_vlan" : access_node['qinqOuterVlan'],      
							"service_vlan" : free_vlan_tag['vlan_tag'], 
							"public_cidr" : client_network,
							"wan_ip" : ip_wan,
							"bandwidth" : bandwidth,
							"datacenter_id" : virtual_pod['datacenterId'] ,
							"resgroup_id" : virtual_pod['resourcePoolId'],
							"datastore_id" : virtual_pod['datastoreId'],
							"wan_portgroup_id" : virtual_pod['uplinkPgId'],
							"lan_portgroup_id" : downlink_pg['dvportgroup_id'],
							"an_client_port" : free_access_port['port'],
							"on_client_port" : client_node_port,
							"on_uplink_port" : client_node['uplink_port']
						 },
				  "devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP']},
							   {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
							   {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']},
							   {"vendor":virtual_pod['vendor'],"model":virtual_pod['model'],"mgmt_ip":virtual_pod['mgmtIP']}]
				}

		#TODO: check if API returns empty values and do rollback
		if ip_wan:
			if client_network:
				pprint(config)
				#Call worker
				ServiceHandler._configure_service(config)
			else:
				service.service_state = ServiceStatuses['ERROR'].value
				service.save()
				print("Not possible service")

	def generate_cpe_mpls_request(params):
		client_name = params['data_model']['client_name']
		location_name = params['data_model']['location']
		service_id = params['data_model']['service_id']
		service_type = params['data_model']['service_type']

		bandwidth  = params['bandwidth']
		client_node_sn = params['client_node_sn']
		client_node_port = params['client_node_port']
		access_port_id = params['access_port_id']
		access_node_id = params['access_node_id']
		vrf_name = params['vrf_name']

		#Get Location by name
		location = ServiceHandler._get_location(location_name)
		location_id = str(location['id'])
		pop_size = location['pop_size']

		router_node = ServiceHandler._get_router_node(location_id)
		router_node_id = str(router_node['id'])
		free_logical_units = ServiceHandler._get_free_logical_units(router_node_id)

		access_node = ServiceHandler._get_access_node(access_node_id)
		free_vlan_tag = ServiceHandler._get_free_vlan_tag(access_node_id)
		free_access_port = ServiceHandler._get_access_node_port(access_port_id)

		#Add vlan tag to access port, serviceid,bandwidth, device SN
		ServiceHandler._add_vlan_tag_to_access_node(free_vlan_tag['vlan_tag'],
													access_node_id,
													access_port_id,
													service_id,
													client_node_sn,
													client_node_port,
													bandwidth)

		client_node = ServiceHandler._get_client_node(client_node_sn)

		vrf = ServiceHandler._get_vrf(vrf_name)
		vrf_id = str(vrf["rt"])
		vrf_exists = ServiceHandler._vrf_exists_in_location(vrf_id,location_id)

		config = {
		   "client" : client_name,
  		   "service_type" : service_type,
  		   "service_id" : service_id,
  		   "op_type" : "CREATE",
  		   "parameters" : {
  		   			"pop_size" : pop_size,       
							"an_uplink_interface" : access_node['uplinkInterface'],
							"an_logical_unit" : free_logical_units[0]['logical_unit_id'],   
							"provider_vlan" : access_node['qinqOuterVlan'],      
							"service_vlan" : free_vlan_tag['vlan_tag'], 
							"bandwidth" : bandwidth,
							"an_client_port" : free_access_port['port'],
							"on_client_port" : client_node_port,
							"vrf_exists": vrf_exists,
            	"vrf_name": vrf['name'],
            	"vrf_id": vrf['rt'],
						},

		 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP'], "loopback":router_node['loopback']},
						 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
						 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]}

		#Make validations
		check_params = True
		if check_params:
			pprint(config)
			#Call worker
			ServiceHandler._configure_service(config)
		else:
			service.service_state = ServiceStatuses['ERROR'].value
			service.save()
			print("Not possible service")



	def generate_cpeless_mpls_request(params):
		client_name = params['data_model']['client_name']
		location_name = params['data_model']['location']
		service_id = params['data_model']['service_id']
		service_type = params['data_model']['service_type']

		client_network = params['client_network']
		prefix = params['prefix']
		bandwidth  = params['bandwidth']
		client_node_sn = params['client_node_sn']
		client_node_port = params['client_node_port']
		access_port_id = params['access_port_id']
		access_node_id = params['access_node_id']
		vrf_name = params['vrf_name']

		client_cidr = client_network + "/" + prefix

		#Get Location by name
		location = ServiceHandler._get_location(location_name)
		location_id = str(location['id'])
		pop_size = location['pop_size']

		router_node = ServiceHandler._get_router_node(location_id)
		router_node_id = str(router_node['id'])
		free_logical_units = ServiceHandler._get_free_logical_units(router_node_id)

		access_node = ServiceHandler._get_access_node(access_node_id)
		free_vlan_tag = ServiceHandler._get_free_vlan_tag(access_node_id)
		free_access_port = ServiceHandler._get_access_node_port(access_port_id)


		#Add vlan tag to access port, serviceid,bandwidth, device SN
		ServiceHandler._add_vlan_tag_to_access_node(free_vlan_tag['vlan_tag'],
													access_node_id,
													access_port_id,
													service_id,
													client_node_sn,
													client_node_port,
													bandwidth)

		client_node = ServiceHandler._get_client_node(client_node_sn)

		vrf = ServiceHandler._get_vrf(vrf_name)
		vrf_id = str(vrf["rt"])
		vrf_exists = ServiceHandler._vrf_exists_in_location(vrf_id,location_id)

		config = {
		   "client" : client_name,
  		   "service_type" : service_type,
  		   "service_id" : service_id,
  		   "op_type" : "CREATE",
  		   "parameters" : {
  		   			"pop_size" : pop_size,       
							"an_uplink_interface" : access_node['uplinkInterface'],
							"an_logical_unit" : free_logical_units[0]['logical_unit_id'],   
							"provider_vlan" : access_node['qinqOuterVlan'],      
							"service_vlan" : free_vlan_tag['vlan_tag'], 
							"bandwidth" : bandwidth,
							"client_cidr" : client_cidr,
							"an_client_port" : free_access_port['port'],
							"on_client_port" : client_node_port,
							"vrf_exists": vrf_exists,
            	"vrf_name": vrf['name'],
            	"vrf_id": vrf['rt'],
						},

		 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP'], "loopback":router_node['loopback']},
						 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
						 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]}

		#Make validations
		check_params = True
		if check_params:
			pprint(config)
			#Call worker
			#ServiceHandler._configure_service(config)
		else:
			service.service_state = ServiceStatuses['ERROR'].value
			service.save()
			print("Not possible service")

