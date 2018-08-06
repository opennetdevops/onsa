from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
from enum import Enum
from pprint import pprint
import requests
import json


class ServiceStatuses(Enum):
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class ServiceView(View):
	IPAM_BASE = "http://10.120.78.90"
	BASE = "http://localhost:8000"

	def get(self, request, service_id=None):
		if service_id is None:
			services = Service.objects.all().values()
			return JsonResponse(list(services), safe=False)
		else:
			service = Service.objects.filter(service_id=service_id).values()[0]
			return JsonResponse(service, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		prefix = data.pop('prefix')
		service_id = data['service_id']

		#CHECK if exists (RETRY option LA VILLA)
		if ServiceView.existing_service(service_id):
			service = Service.objects.filter(service_id=service_id)
			service.update(**data)
		else:
			service = Service.objects.create(**data)

		service = Service.objects.get(service_id=service_id)
		service.service_state = ServiceStatuses['REQUESTED'].value
		service.save()
		

		if service.service_type == "vcpe_irs" :
			ServiceView.generate_vcpe_irs_request(service,prefix)

		response = {"message" : "Service requested"}
		return JsonResponse(response)

	def put(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.filter(service_id=service_id)
		service.update(**data)
		data = serializers.serialize('json', service)
		return HttpResponse(data, content_type='application/json')

	def generate_vcpe_irs_request(service,prefix):
		ip_wan = ServiceView.get_ip_wan_nsx(service.location,service.client_name,service.service_id)
		public_network = ServiceView.get_public_network(service.client_name,service.service_id,prefix)
		location_id = str(ServiceView.get_location_id(service.location))
		virtual_pod = ServiceView.get_virtual_pod(location_id)
		router_node = ServiceView.get_router_node(location_id)
		downlink_pg = ServiceView.get_virtual_pod_downlink_portgroup(str(virtual_pod['id']))
		router_node_id = str(router_node['id'])
		free_logical_units = ServiceView.get_free_logical_units(router_node_id)
		free_access_port = ServiceView.get_free_access_port(location_id)
		access_port_id = str(free_access_port['id'])
		access_node_id = str(free_access_port['accessNode_id'])
		access_node = ServiceView.get_access_node(access_node_id)
		free_vlan_tag = ServiceView.get_free_vlan_tag(access_port_id)

		config = {
	   "client":service.client_name,
	   "service_type":service.service_type,
	   "service_id":service.service_id,
	   "op_type":"CREATE",
	   "devices":[
	      {  
	         "model":router_node['model'],
	         "parameters":{
	            "mgmt_ip":router_node['mgmtIP'],    
	            "vmw_uplinkInterface":virtual_pod['uplinkInterface'], 
	            "vmw_logicalUnit":free_logical_units[0]['logical_unit_id'],  
	            "vmw_vlan":downlink_pg['vlan_tag'],           
	            "an_uplinkInterface":access_node['uplinkInterface'],  
	            "an_logicalUnit":free_logical_units[1]['logical_unit_id'],   
	            "an_qinqOuterVlan":access_node['qinqOuterVlan'],      
	            "an_qinqInnerVlan":free_vlan_tag['vlan_tag'],     
	            "public_cidr":public_network
	         }
	      },
	      {  
	      	"model":virtual_pod['model'],
          "parameters":{
            "datacenterMoid":virtual_pod['datacenterId'], 
            "resourcePoolId":virtual_pod['resourcePoolId'], 
            "datastoreId":virtual_pod['datastoreId'],     
		        "uplink":{
		          "portgroupId":virtual_pod['uplinkPgId'], 
		          "primaryAddress":ip_wan
		        },
		         "downlink":{
		         	"portgroupId":downlink_pg['dvportgroup_id'],
		         	"public_cidr":public_network
		         }
	         }
	      },
	      {  
         "model":access_node['model'],
         "parameters":{
            "mgmt_ip" : access_node['mgmtIP'],
            "service_vlan": free_vlan_tag['vlan_tag'],
            "client_port": free_access_port['port']
         }
      }
	   ]
		}

		#TODO: check if API returns empty values and do rollback
		if ip_wan:
			if public_network:
				#Call worker
				pprint(config)
				ServiceView.configure_service(config)
			else:
				service.service_state = ServiceStatuses['ERROR'].value
				service.save()
				print("Not possible service")		
		

	def configure_service(config):
		url = "/worker/api/services"
		rheaders = {'Content-Type': 'application/json'}
		data = config
		response = requests.post(ServiceView.BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

	def get_ipam_authentication_token():
		url = "/api/authenticate"
		rheaders = {'Content-Type': 'application/json'}
		#App User
		data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
		response = requests.post(ServiceView.IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)['auth_token']


	def get_ip_wan_nsx(location,client_name,service_id):
		description = client_name + "-" + service_id
		#"Searchin by owner prefix=WAN_NSX"
		owner = "WAN_NSX_" + location
		token = ServiceView.get_ipam_authentication_token()
		url = "/api/networks/assign_ip"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		data = {"description":description,"owner":owner,"ip_version":4}
		response = requests.post(ServiceView.IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if "network" in json_response:
			return json_response["network"]
		else:
			return None

	def get_public_network(client_name,service_id,mask):
		description = client_name + "-" + service_id
		owner = "PUBLIC_ONSA"
		token = ServiceView.get_ipam_authentication_token()
		url = "/api/networks/assign_subnet"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
		response = requests.post(ServiceView.IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if "network" in json_response:
			return json_response["network"]
		else:
			return None

	def get_location_id(location_name):
		url= "/inventory/api/locations?name="+location_name
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]['id']
		else:
			return None

	def get_router_node(location_id):
		url= "/inventory/api/locations/"+ location_id + "/routernodes"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def get_virtual_pod(location_id):
		url= "/inventory/api/locations/"+ location_id + "/virtualpods"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def get_virtual_pod_downlink_portgroup(virtual_pod_id):
		url= "/inventory/api/virtualpods/"+ virtual_pod_id + "/portgroups?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def get_free_logical_units(router_node_id):
		url= "/inventory/api/routernodes/" + router_node_id + "/logicalunits?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		#TODO check minimum size = 2
		if json_response:
			return json_response
		else:
			return None

	def add_logical_unit_to_router_node(router_node_id,logical_unit_id):
		url= "/inventory/api/routernodes/" + router_node_id + "/logicalunits"
		rheaders = {'Content-Type': 'application/json'}
		data = {"logical_unit_id":logical_unit_id}
		response = requests.post(ServiceView.BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None


	def get_free_access_port(location_id):
		url= "/inventory/api/locations/"+ location_id + "/accessports?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def use_port(access_port_id):
		url= "/inventory/api/accessports/" + access_port_id
		rheaders = {'Content-Type': 'application/json'}
		data = {"userd":True}
		response = requests.post(ServiceView.BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def get_access_node(access_node_id):
		url= "/inventory/api/accessnodes/"+ access_node_id 
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def get_free_vlan_tag(access_port_id):
		url= "/inventory/api/accessports/"+ access_port_id + "/vlantags?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def add_vlan_tag_to_access_port(vlan_tag,access_port_id):
		url= "/inventory/api/accessports/"+ access_port_id + "/vlantags"
		rheaders = {'Content-Type': 'application/json'}
		data = {"vlan_tag":vlan_tag}
		response = requests.post(ServiceView.BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def existing_service(service_id):
		return Service.objects.filter(service_id=service_id).count() is not 0
