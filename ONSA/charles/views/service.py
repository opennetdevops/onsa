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

	def get(self, request):
		services = Service.objects.all().values()
		return JsonResponse(list(services), safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.create(**data)
		service.service_state = ServiceStatuses['REQUESTED'].value
		# service.save()
		location = service.location

		#Make request to worker with all data needed
		public_ip = ServiceView.get_public_ip()
		nsx_wan = ServiceView.get_nsx_wan(location)

		print(public_ip)
		print(nsx_wan)


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


	def get_public_ip():
		token = ServiceView.get_ipam_authentication_token()
		url = "/api/networks"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		response = requests.get(ServiceView.IPAM_BASE + url, auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)

	def get_nsx_wan(location):
		token = ServiceView.get_ipam_authentication_token()
		url = "/api/networks"
		rheaders = {'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + token}
		response = requests.get(ServiceView.IPAM_BASE + url, auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)
		
