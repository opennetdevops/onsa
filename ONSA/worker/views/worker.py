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

		pending_tasks = []
		executed_tasks = []
		for device in data['devices']:
			pending_tasks.append(Task.factory(data['service_type'], service))


		for task in pending_tasks:
			task.run_task()


		response = {"message" : "created"}
		return JsonResponse(response)

	def put(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		data = serializers.serialize('json',)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request):		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')