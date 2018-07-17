from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View



from pprint import pprint

from ..models import Service, Task

import requests
import json

from ..lib.juniper.mx_config import *
from ..lib.nsx.edge import *

CHARLES = "http://localhost:8000"

class WorkerView(View):
	def get(self, request):
		data = {"message" : "test"}
		return JsonResponse(data, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		"""
		Create service based on:

		service_id: Service identifier

		service_type: Can be any type of service, such as
		VCPE-IRS, VCPE-MPLS, CPE-IRS, CPE-MPLS, CPELESS-IRS, CPELESS-MPLS

		service_state: Status of the actual service after being requested

		"""

		service = Service(service_id=data['service_id'], service_type=data['service_type'], service_state="In Progress")
		service.save()

		"""
		Creates all of the tasks associated with
		the service requested.
		"""

		for device in data['devices']:
			task = Task.factory(device['model'], service.service_type, service, device['parameters'])
			task.save()

		"""
		Runs all of the tasks in the background.
		"""
		service.deploy(service_id=service.service_id)
		
		"""
		Updates Charles' service status	
		"""

		USER = "admin"
		PASS = "F1b3rc0rp!"
		rheaders = {'Content-Type': 'application/json'}
		requests.put(CHARLES+"/api/charles/services/%s" % service.service_id, data = data, auth = (USER, PASS), verify = False, headers = rheaders)

		return HttpResponse("")