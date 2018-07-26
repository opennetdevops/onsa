from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
from enum import Enum
import requests
import json


class ServiceStatuses(Enum):
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class ServiceView(View):
	IPAM_BASE = "http://10.120.78.90"
	INVENTORY_BASE = "http://localhost:8000"

	def get(self, request, service_id=None):
		if service_id is None:
			services = Service.objects.all().values()
		else:
			services = Service.objects.filter(service_id=service_id).values()
			
		return JsonResponse(list(services), safe=False)

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
		response = requests.get(ServiceView.INVENTORY_BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]['id']
		else:
			return None

	def get_virtual_pod(location_id):
		url= "/inventory/api/locations/"+ location_id + "/virtualpods"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.INVENTORY_BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def get_virtual_pod_downlink_portgroup(virtual_pod_id):
		url= "/inventory/api/virtualpods/"+ virtual_pod_id + "/portgroups?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(ServiceView.INVENTORY_BASE + url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def existing_service(service_id):
		return Service.objects.filter(service_id=service_id).count() is not 0

	def generate_vcpe_irs_request(service,prefix):
		ip_wan = ServiceView.get_ip_wan_nsx(service.location,service.client_name,service.service_id)
		public_network = ServiceView.get_public_network(service.client_name,service.service_id,prefix)
		location_id = str(ServiceView.get_location_id(service.location))
		virtual_pod = ServiceView.get_virtual_pod(location_id)
		downlink_pg = ServiceView.get_virtual_pod_downlink_portgroup(str(virtual_pod['id']))

		if ip_wan:
			if public_network:
				print(ip_wan)
				print(public_network)
				print(location_id)
				print(virtual_pod)
				print(downlink_pg)
			else:
				service.service_state = ServiceStatuses['ERROR'].value
				service.save()
				print("Not possible service")		
		
