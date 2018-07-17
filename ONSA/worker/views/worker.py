from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View



from pprint import pprint

from ..models import Service, Task


import json

from ..lib.juniper.mx_config import *
from ..lib.nsx.edge import *

class WorkerView(View):
	def get(self, request):
		data = {"message" : "test"}
		return JsonResponse(data, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		service = Service(service_id=data['service_id'], service_type=data['service_type'], service_state="In Progress")
		service.save()

		for device in data['devices']:
			task = Task.factory(device['model'], service.service_type, service, device['parameters'])
			task.save()

		service.deploy(service_id=service.service_id)
		

		return HttpResponse("")

	def put(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		data = serializers.serialize('json',)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request):		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')