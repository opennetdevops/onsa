from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
from enum import Enum
import json

class ServiceStatuses(Enum):
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class ServiceView(View):

	def get(self, request):
		services = Service.objects.all().values()
		return JsonResponse(list(services), safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service(service_id=data['service_id'], service_type=data['service_type'],
		 service_state=ServiceStatuses['REQUESTED'].value, client_id=data['client_id'],
		  client_name=data['client_name'] )
		service.save()
		response = {"message" : "Service requested"}


		#Make request to worker with all data needed

		return JsonResponse(response)

	def put(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.filter(service_id=service_id)
		service.update(**data)
		data = serializers.serialize('json', service)
		return HttpResponse(data, content_type='application/json')