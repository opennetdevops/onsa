from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from pprint import pprint

from itertools import chain

from ..models import Service, Task

import json

class WorkerView(View):
	def get(self, request, service_id=None):
		# state = request.GET.get('status', '')
		if service_id is None:
			my_services = Service.objects.all().values()			
			return JsonResponse(list(chain(my_services)), safe=False)
	
	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		"""
		Create service based on:

		service_id: Service identifier

		service_type: Can be any type of service, such as
		VCPE-IRS, VCPE-MPLS, CPE-IRS, CPE-MPLS, CPELESS-IRS, CPELESS-MPLS

		service_state: Status of the actual service after being requested

		"""

		service = Service(client_name=data['client'],
						service_id=data['service_id'],
						service_type=data['service_type'],
						service_state="IN_PROGRESS",
						parameters=data['parameters'])
		service.save()

		"""
		Creates all of the tasks associated with
		the service requested.
		"""
		for device in data['devices']:
			task = Task(service=service,
						op_type=data['op_type'],
						device=device)
			task.save()

		"""
		Runs all of the tasks in the background.
		"""
		service.deploy(service_id=service.service_id)

		return HttpResponse(status=202)