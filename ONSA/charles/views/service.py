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

	def get(self, request, service_id=None):
		if service_id is None:
			services = Service.objects.all().values()
		else:
			services = Service.objects.filter(service_id=service_id).values()
			
		return JsonResponse(list(services), safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		
		#CHECK if exists (RETRY option)
		if Service.objects.filter(service_id=data['service_id']).count() is not 0:
			service = Service.objects.filter(service_id=data['service_id'])
			service.update(**data)
		else:
			service = Service.objects.create(**data)

		service = Service.objects.get(service_id=data['service_id'])
		service.service_state = ServiceStatuses['REQUESTED'].value
		#todo - hint - se va a romper cuando le pase el prefix
		service.save()
		
		location = service.location

		#Make request to worker with all data needed
		mask = 28 #Depends on service type
		#todo fix?
		public_ip = ServiceView.get_ip_wan_nsx(service.location,service.client_name,service.service_id)
		nsx_wan = ServiceView.get_public_network(service.client_name,service.service_id,28)

		if "network" in public_ip and "network" in nsx_wan:
			#ask for devices 
			print(public_ip["network"])
			print(nsx_wan["network"])
		else:
			print("Not possible service")


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
		data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
		response = requests.post(ServiceView.IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)['auth_token']


	def get_ip_wan_nsx(location,client_name,service_id):
		description = client_name + "-" + service_id
		owner = "WAN_NSX_" + location
		token = ServiceView.get_ipam_authentication_token()
		url = "/api/networks/assign_ip"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		data = {"description":description,"owner":owner,"ip_version":4}
		response = requests.post(ServiceView.IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)

	def get_public_network(client_name,service_id,mask):
		description = client_name + "-" + service_id
		owner = "PUBLIC_ONSA"
		token = ServiceView.get_ipam_authentication_token()
		url = "/api/networks/assign_subnet"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
		response = requests.post(ServiceView.IPAM_BASE + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)
		
