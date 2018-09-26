from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
from ..services import ServiceHandler
from enum import Enum
from pprint import pprint
import requests
import json

class ServiceStatuses(Enum):
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class ServiceView(View):

	def get(self, request, service_id=None):
		if service_id is None:
			services = Service.objects.all().values()
			return JsonResponse(list(services), safe=False)
		else:
			service = Service.objects.filter(service_id=service_id).values()[0]
			return JsonResponse(service, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service_id = data['data_model']['service_id']
		#Check if exists (retry support)
		if ServiceView.existing_service(service_id):
			service = Service.objects.filter(service_id=service_id)
			service.update(**data['data_model'])
		else:
			service = Service.objects.create(**data['data_model'])

		service = Service.objects.get(service_id=service_id)
		service.service_state = ServiceStatuses['REQUESTED'].value
		service.save()

		generate_request = getattr(ServiceHandler.ServiceHandler, "generate_" + service.service_type + "_request")

		generate_request(data)
		
		response = { "message" : "Service Requested." }

		return JsonResponse(response)

	def put(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.filter(service_id=service_id)
		service.update(**data)
		data = serializers.serialize('json', service)

		#Update service status in core
		data = {
			"service_state":service[0].service_state
		}

		#Rollback all reservations if error
		if service[0].service_state == ServiceStatuses['ERROR'].value:
			ServiceView.rollback_service(str(service_id))

		ServiceView.update_core_service_status(str(service_id))

		return HttpResponse(data, content_type='application/json')

	def existing_service(service_id):
		return Service.objects.filter(service_id=service_id).count() is not 0

	def rollback_service(service_id):
		url = "/api/products/" + service_id + "/rollback"
		r = requests.post(url)

	def update_core_service_statuste(service_id):
		headers = {'Content-Type': 'application/json'}
		url = settings.CORE_URL +"services/" + service_id
		r = requests.put(url, data = json.dumps(data), headers=rheaders)
		