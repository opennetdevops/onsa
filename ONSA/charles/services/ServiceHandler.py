from django.conf import settings

from pprint import pprint
import requests
import json
from ..views.service import *

WAN_MPLS_MASK = 30

class ServiceHandler():

	def _configure_service(config):
		url = settings.WORKER_URL + "services"
		rheaders = {'Content-Type': 'application/json'}
		data = config
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

	def _get_ipam_authentication_token():
		url = "/api/authenticate"
		rheaders = {'Content-Type': 'application/json'}
		#App User
		data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
		response = requests.post(settings.IPAM_URL + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)['auth_token']


	def _get_ip_wan_nsx(location,client_name,service_id):
		description = client_name + "-" + service_id
		#"Searchin by owner prefix=WAN_NSX"
		owner = "WAN_NSX_" + location
		token = ServiceHandler._get_ipam_authentication_token()
		url = settings.IPAM_URL + "/api/networks/assign_ip"
		rheaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
		data = { "description" : description, "owner" : owner,"ip_version" : 4 }
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if "network" in json_response:
			return json_response["network"]
		else:
			return None

	def _get_wan_mpls_network(location,client_name,service_id):
		#Default prefix set by IDR
		mask = 30
		description = client_name + "-" + service_id
		owner = "WAN_MPLS_" + location
		token = ServiceHandler._get_ipam_authentication_token()
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

	def _get_client_network(client_name,service_id,mask):
		description = client_name + "-" + service_id
		owner = "PUBLIC_ONSA"
		token = ServiceHandler._get_ipam_authentication_token()
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

	def _get_location(location_name):
		url = settings.INVENTORY_URL + "locations?name="+location_name
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_router_node(location_id):
		url= settings.INVENTORY_URL + "locations/"+ location_id + "/routernodes"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_virtual_pod(location_id):
		url= settings.INVENTORY_URL + "locations/"+ location_id + "/virtualpods"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_client_node(client_node_sn):
		url= settings.INVENTORY_URL + "clientnodes/"+client_node_sn
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_virtual_pod_downlink_portgroup(virtual_pod_id):
		url= settings.INVENTORY_URL + "virtualpods/"+ virtual_pod_id + "/portgroups?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _use_portgroup(portgroup_id):
		url= settings.INVENTORY_URL + "portgroups/" + portgroup_id
		rheaders = {'Content-Type': 'application/json'}
		data = {"used":True}
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_free_logical_units(router_node_id):
		url = settings.INVENTORY_URL + "routernodes/" + router_node_id + "/logicalunits?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		#TODO check minimum size = 2
		if json_response:
			return json_response
		else:
			return None

	def _add_logical_unit_to_router_node(router_node_id,logical_unit_id,product_id):
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

	def _get_free_access_port(location_id):
		url= settings.INVENTORY_URL + "locations/"+ location_id + "/accessports?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _use_port(access_port_id):
		url= settings.INVENTORY_URL + "accessports/" + access_port_id
		rheaders = {'Content-Type': 'application/json'}
		data = {"used":True}
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_access_node(access_node_id):
		url= settings.INVENTORY_URL + "accessnodes/"+ access_node_id 
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_free_vlan_tag(access_port_id):
		url= settings.INVENTORY_URL + "accessnodes/"+ access_port_id + "/vlantags?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _add_vlan_tag_to_access_node(vlan_tag,access_node_id,access_port_id,service_id,client_node_sn,client_node_port,bandwidth,vrf_id=None):
		url= settings.INVENTORY_URL + "accessnodes/"+ access_node_id + "/vlantags"
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

	def _add_product(vlan_tag,access_node_id,access_port_id,service_id,client_node_sn,client_node_port,bandwidth,vrf_id=None):
		url= settings.INVENTORY_URL + "products"
		rheaders = {'Content-Type': 'application/json'}
		data = {"access_node_id":access_node_id,
				"vlan_tag":vlan_tag,
				"product_id":service_id,
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

	def _get_access_node_port(access_port_id):
		url= settings.INVENTORY_URL + "accessports/"+ access_port_id 
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _get_vrf(vrf_name):
		url = settings.INVENTORY_URL + "vrfs?" + "name=" + vrf_name
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def _vrf_exists_in_location(vrf_id,location_id):
		url = settings.INVENTORY_URL + "vrfs/" + vrf_id + "/locations/" + location_id
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response["exists"]
		else:
			return None

	def _add_location_to_vrf(vrf_id,location_id):
		url = settings.INVENTORY_URL + "vrfs/" + vrf_id + "/locations/" + location_id
		rheaders = {'Content-Type': 'application/json'}
		response = requests.put(url, auth = None, verify = False, headers = rheaders)

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

		location = ServiceHandler._get_location(location_name)
		location_id = str(location['id'])
		pop_size = location['pop_size']
		router_node = ServiceHandler._get_router_node(location_id)
		router_node_id = str(router_node['id'])
		free_logical_units = ServiceHandler._get_free_logical_units(router_node_id)
		access_port_id = params['access_port_id']
		access_node_id = params['access_node_id']
		access_node = ServiceHandler._get_access_node(access_node_id)
		free_vlan_tag = ServiceHandler._get_free_vlan_tag(access_node_id)
		free_access_port = ServiceHandler._get_access_node_port(access_port_id)

		#Get client node by SN
		client_node = ServiceHandler._get_client_node(client_node_sn)

		error = False

		if free_logical_units and free_vlan_tag:
			client_network = ServiceHandler._get_client_network(client_name,service_id,prefix)
			if client_network:
				#Add logicals unit to routernode
				ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'],service_id)
				#Add vlan tag to access port, serviceid,bandwidth, device SN
				ServiceHandler._add_product(free_vlan_tag['vlan_tag'],
														access_node_id,
														access_port_id,
														service_id,
														client_node_sn,
														client_node_port,
														bandwidth)
				config = {
				   "client" : client_name,
		  		   "service_type" : service_type,
		  		   "service_id" : service_id,
		  		   "op_type" : "CREATE",
		  		   "parameters" : {
		  		   			"pop_size" : pop_size,       
									"an_uplink_interface" : access_node['uplinkInterface'],
									"an_uplink_ports" : access_node['uplink_ports'],
									"logical_unit" : free_logical_units[0]['logical_unit_id'],   
									"provider_vlan" : access_node['qinqOuterVlan'],      
									"service_vlan" : free_vlan_tag['vlan_tag'], 
									"client_cidr" : client_network,
									"bandwidth" : bandwidth,
									"an_client_port" : free_access_port['port'],
									"on_client_port" : client_node_port,
									"on_uplink_port" : client_node['uplink_port']
								},

				 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP']},
								 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
								 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]
				}
				pprint(config)
				# ServiceHandler._configure_service(config)
			else:
				error = True
		else:
			error = True

		if error:
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

		location = ServiceHandler._get_location(location_name)
		location_id = str(location['id'])

		virtual_pod = ServiceHandler._get_virtual_pod(location_id)
		router_node = ServiceHandler._get_router_node(location_id)
		downlink_pg = ServiceHandler._get_virtual_pod_downlink_portgroup(str(virtual_pod['id']))
		portgroup_id = str(downlink_pg['id'])
		free_access_port = ServiceHandler._get_access_node_port(access_port_id)
		router_node_id = str(router_node['id'])
		free_logical_units = ServiceHandler._get_free_logical_units(router_node_id)
		access_node = ServiceHandler._get_access_node(access_node_id)
		free_vlan_tag = ServiceHandler._get_free_vlan_tag(access_node_id)
		#Get client node by SN
		client_node = ServiceHandler._get_client_node(client_node_sn)
		lu_size = len(free_logical_units)

		error = False

		if free_vlan_tag and lu_size>=2 and downlink_pg:
			ip_wan = ServiceHandler._get_ip_wan_nsx(location_name, client_name, service_id)
			if ip_wan:
				client_network = ServiceHandler._get_client_network(client_name, service_id, prefix)
				if client_network:
					#Add vlan tag to access port, serviceid,bandwidth, device SN
					ServiceHandler._add_product(free_vlan_tag['vlan_tag'],
																access_node_id,
																access_port_id,
																service_id,
																client_node_sn,
																client_node_port,
																bandwidth)
					#Use porgroup
					ServiceHandler._use_portgroup(portgroup_id)
					#Add logicals unit to routernode
					ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'],service_id)
					ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[1]['logical_unit_id'],service_id)
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
										"client_cidr" : client_network,
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
					pprint(config)
					#Call worker
					# ServiceHandler._configure_service(config)
				else:
					#TODO: Free wan_ip
					error = True
			else:
				error = True
		else:
			error = True

		if error:
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
		client_as = params['client_as']

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
		client_node = ServiceHandler._get_client_node(client_node_sn)
		vrf = ServiceHandler._get_vrf(vrf_name)
		vrf_id = str(vrf["rt"])
		vrf_exists = ServiceHandler._vrf_exists_in_location(vrf_id,location_id)

		error = False

		if free_logical_units and free_vlan_tag:
			wan_cidr = ServiceHandler._get_wan_mpls_network(location_name, client_name, service_id)
			if wan_cidr: 
				if not vrf_exists:
					ServiceHandler._add_location_to_vrf(vrf_id,location_id)
				#Add logical unit to router node
				ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'],service_id)
				#Add vlan tag to access port, serviceid,bandwidth, device SN
				ServiceHandler._add_product(free_vlan_tag['vlan_tag'],
															access_node_id,
															access_port_id,
															service_id,
															client_node_sn,
															client_node_port,
															bandwidth,
															vrf_id)
				config = {
				   "client" : client_name,
		  		   "service_type" : service_type,
		  		   "service_id" : service_id,
		  		   "op_type" : "CREATE",
		  		   "parameters" : {
		  		   			"pop_size" : pop_size,       
									"an_uplink_interface" : access_node['uplinkInterface'],
									"an_uplink_ports" :   access_node['uplink_ports'],
									"logical_unit" : free_logical_units[0]['logical_unit_id'],   
									"provider_vlan" : access_node['qinqOuterVlan'],      
									"service_vlan" : free_vlan_tag['vlan_tag'], 
									"bandwidth" : bandwidth,
									"client_as_number" : client_as,
									"an_client_port" : free_access_port['port'],
									"on_client_port" : client_node_port,
									"vrf_exists": vrf_exists,
									"wan_cidr": wan_cidr,
									"client_cidr": " ",
		            	"vrf_name": vrf['name'],
		            	"vrf_id": vrf['rt'],
		            	"loopback":router_node['loopback']
								},
				 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP']},
								 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
								 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]}

				pprint(config)
				#Call worker
				# ServiceHandler._configure_service(config)
			else:
				error = True
		else:
			error = True

		if error:
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

		vrf = ServiceHandler._get_vrf(vrf_name)
		vrf_id = str(vrf["rt"])
		vrf_exists = ServiceHandler._vrf_exists_in_location(vrf_id,location_id)

		client_node = ServiceHandler._get_client_node(client_node_sn)

		if free_logical_units and free_vlan_tag:
			#Add vlan tag to access port, serviceid,bandwidth, device SN
			ServiceHandler._add_product(free_vlan_tag['vlan_tag'],
														access_node_id,
														access_port_id,
														service_id,
														client_node_sn,
														client_node_port,
														bandwidth,
														vrf_id)
			#Add logical unit to router node
			ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'],service_id)
			if not vrf_exists:
				ServiceHandler._add_location_to_vrf(vrf_id,location_id)

			config = {
			   "client" : client_name,
	  		   "service_type" : service_type,
	  		   "service_id" : service_id,
	  		   "op_type" : "CREATE",
	  		   "parameters" : {
	  		   			"pop_size" : pop_size,       
								"an_uplink_interface" : access_node['uplinkInterface'],
								"an_uplink_ports" :   access_node['uplink_ports'],
								"logical_unit" : free_logical_units[0]['logical_unit_id'],   
								"provider_vlan" : access_node['qinqOuterVlan'],      
								"service_vlan" : free_vlan_tag['vlan_tag'], 
								"bandwidth" : bandwidth,
								"client_cidr" : client_cidr,
								"an_client_port" : free_access_port['port'],
								"on_client_port" : client_node_port,
								"vrf_exists": vrf_exists,
	            	"vrf_name": vrf['name'],
	            	"vrf_id": vrf['rt'],
	            	"loopback":router_node['loopback']
							},
			 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP']},
							 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
							 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]}

			pprint(config)
			#Call worker
			# ServiceHandler._configure_service(config)
		else:
			service.service_state = ServiceStatuses['ERROR'].value
			service.save()
			print("Not possible service")

	def generate_vpls_request(params):
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

		vrf = ServiceHandler._get_vrf(vrf_name)
		vrf_id = str(vrf["rt"])
		vrf_exists = ServiceHandler._vrf_exists_in_location(vrf_id,location_id)

		client_node = ServiceHandler._get_client_node(client_node_sn)

		if free_logical_units and free_vlan_tag:
			#Add vlan tag to access port, serviceid,bandwidth, device SN
			ServiceHandler._add_product(free_vlan_tag['vlan_tag'],
														access_node_id,
														access_port_id,
														service_id,
														client_node_sn,
														client_node_port,
														bandwidth,
														vrf_id)

			#Add logical unit to router node
			ServiceHandler._add_logical_unit_to_router_node(router_node_id,free_logical_units[0]['logical_unit_id'],service_id)
			if not vrf_exists:
				ServiceHandler._add_location_to_vrf(vrf_id,location_id)

			config = {
			   "client" : client_name,
	  		   "service_type" : service_type,
	  		   "service_id" : service_id,
	  		   "op_type" : "CREATE",
	  		   "parameters" : {
	  		   			"pop_size" : pop_size,       
								"an_uplink_interface" : access_node['uplinkInterface'],
								"an_uplink_ports" :   access_node['uplink_ports'],
								"logical_unit" : free_logical_units[0]['logical_unit_id'],   
								"provider_vlan" : access_node['qinqOuterVlan'],      
								"service_vlan" : free_vlan_tag['vlan_tag'], 
								"bandwidth" : bandwidth,
								"an_client_port" : free_access_port['port'],
								"on_client_port" : client_node_port,
								"vrf_exists": vrf_exists,
	            	"vrf_name": vrf['name'],
	            	"vrf_id": vrf['rt'],
	            	"loopback":router_node['loopback']
							},
			 	"devices" : [{"vendor":router_node['vendor'],"model":router_node['model'],"mgmt_ip":router_node['mgmtIP']},
							 {"vendor":access_node['vendor'],"model":access_node['model'],"mgmt_ip":access_node['mgmtIP']},
							 {"vendor":client_node['vendor'],"model":client_node['model'],"mgmt_ip":client_node['mgmtIP']}]}

			pprint(config)
			#Call worker
			#ServiceHandler._configure_service(config)
		else:
			service.service_state = ServiceStatuses['ERROR'].value
			service.save()
			print("Not possible service")
