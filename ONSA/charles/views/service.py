from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from charles.models import Service
from charles.utils.fsm import Fsm
from enum import Enum
from charles.utils.utils import *
from pprint import pprint
import requests
import json


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

		# Retry support
		if not self._existing_service(data['service_id']):
			charles_service = Service.objects.create(service_id=data['service_id'], target_state=data['target_state'], deployment_mode=data['deployment_mode'])
		else:
			charles_service = Service.objects.get(service_id=data['service_id'])
			charles_service.target_state = data['target_state']
			charles_service.deployment_mode = data['deployment_mode']


		service = get_service(data['service_id'])
		charles_service.service_state = service['service_state']

		#for persistence
		charles_service.save()

		my_charles_service = Service.objects.filter(service_id=data['service_id']).values()[0]
		my_charles_service.update(service)


		pprint(my_charles_service)

		service_state = Fsm.run(my_charles_service)
		pprint(request)
		
		if service_state is not None:
			charles_service.service_state = service_state
			response = { "message": "Service requested." }
		else:
			charles_service.service_state = "error"
			response = { "message": "Service request failed." }
		
		charles_service.save()
		return JsonResponse(response)

	def put(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		# if data['service_state'] != "ERROR":
		# 	service = Service.objects.get(service_id=service_id)
		# 	service.service_state = NextStateE2e[service.service_state].value
		# 	service.save()

		# 	update_service(service_id, {'service_state': service.service_state})

		# 	if service.service_state != service.target_state:
		# 		service = get_service(service_id)
		# 		client = get_client(service['client_id'])

		# 		generate_request = getattr(ServiceTypes[service['service_type']].value, "generate_" + service['service_type'] + "_request")
		# 		request, service_state = generate_request(client, service, code="cpe")
		# 		pprint(request)

		# # Rollback all reservations if error
		# # if service[0].service_state == "ERROR":
		# # 	rollback_service(str(service_id))	

		response = { "message": "Service stated updated" }

		return JsonResponse(response, safe=False)


	def _existing_service(self, service_id):
	    return Service.objects.filter(service_id=service_id).count() is not 0



class ProcessView(View):

	def post(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.get(service_id=service_id)

		if service.process_worker_response(data['service_state']) != "error":
			data = {'service_state': service.service_state}
			update_service(service.service_id, data)
			response = { "message": "Service stated updated" }
		else:
			data = {'service_state': "error"}
			update_service(service.service_id, data)
			response = { "message": "Service update failed" }
		
		return JsonResponse(response, safe=False)



