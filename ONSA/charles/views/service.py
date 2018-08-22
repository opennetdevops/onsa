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
		return HttpResponse(data, content_type='application/json')

	def existing_service(service_id):
		return Service.objects.filter(service_id=service_id).count() is not 0