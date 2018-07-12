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

		service = Service(service_id=data['service_id'], service_type=data['service_type'], service_state="Requested")
		service.save()

		# # ToDo: Transitions
		for device in data['devices']:
			task = Task.factory(model=device['model'], service_type=data['service_type'], service=service)
			task.save()
			task_state = task.run_task(device['parameters'], data['tasks_type'])

		response = {"message" : "created"}
		return JsonResponse(response)

	def put(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		data = serializers.serialize('json',)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request):		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')