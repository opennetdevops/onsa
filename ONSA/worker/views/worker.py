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

		pending_tasks = []
		executed_tasks = []
		failed_tasks = []
		devices = []


		for device in data['devices']:
			pending_tasks.append(Task.factory(device['model'], service.service_type, service))
			devices.append(device)


		num_of_tasks = len(pending_tasks)
		pprint(num_of_tasks)

		for i in range(0,num_of_tasks):

			task = pending_tasks.pop(0)
			device = devices.pop(0)

			pprint(task)
			pprint(device)

			task_state = task.run_task(device)
			if task_state:
				executed_tasks.append(task)
			else:
				failed_tasks.append(task)

			# ToDo:
			# else:
			# 	task.rollback()
			# 	break

		# for task in executed_tasks:
		# 	# task_state = task.rollback() #ToDo:
		# 	print("ToDo")

		# ToDo: PUT /charles

		pprint(executed_tasks)

		return HttpResponse("")

	def put(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		data = serializers.serialize('json',)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request):		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')