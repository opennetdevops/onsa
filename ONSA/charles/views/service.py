from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
import json

class ServiceView(View):

	def post(self, request):
		pass
		# data = json.loads(request.body.decode(encoding='UTF-8'))

		# service = Service(service_id=data['service_id'], service_type=data['service_type'], service_state="Requested")
		# service.save()

		# # # ToDo: Transitions
		# for device in data['devices']:
		# 	task = Task.factory(model=device['model'], service_type=data['service_type'], service=service)
		# 	task.save()
		# 	task_state = task.run_task(device['parameters'], data['tasks_type'])

		# response = {"message" : "created"}
		# return JsonResponse(response)

	def put(self, request):
		pass
		# data = json.loads(request.body.decode(encoding='UTF-8'))

		# data = serializers.serialize('json',)
		# return HttpResponse(data, content_type='application/json')