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

# class ServiceTypes(Enum):
#     cpeless_irs = cpeless_irs_service
#     cpe_mpls = cpe_mpls_service
#     cpeless_mpls = cpeless_mpls_service
#     vcpe_irs = vcpe_irs_service
#     vpls = vpls_service

class CodeMap(Enum):
    e2e = "bb"
    bb = "bb"
    bb_data = "bb_data"
    cpe_data = "cpe_data"
    an = "an"

class NextStateE2e(Enum):
    BB_ACTIVATION_IN_PROGRESS = "BB_ACTIVATED"
    BB_ACTIVATED = "SERVICE_ACTIVATED"
    CPE_ACTIVATION_IN_PROGRESS = "SERVICE_ACTIVATED"




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

		service = get_service(data['service_id'])
		client = get_client(service['client_id'])
		customer_location = get_customer_location(service['client_id'], service['customer_location_id'])

		# TODO ARI NO TE OLVIDES DE ESTO
		# client_port_id = self.fetch_cpe(data, service, client, customer_location) if data['activation_code'] == "e2e" or data['activation_code'] == "cpe_data" else None 
		# if client_port_id:
		# 	service_data = { "client_port_id": client_port_id }
		# 	update_service(data['service_id'], service_data)


		# Retry support
		if not self._existing_service(data['service_id']):
			charles_service = Service.objects.create(service_id=data['service_id'], target_state=data['target_state'])
		else:
			charles_service = Service.objects.get(service_id=data['service_id'])
			charles_service.target_state = data['target_state']


		service = get_service(data['service_id'])

		# generate_request = getattr(ServiceTypes[service['service_type']].value, "generate_" + service['service_type'] + "_request")
		# request, service_state = generate_request(client, service, CodeMap[data['activation_code']].value)
		service_state = Fsm.run(service)

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

		if data['service_state'] != "ERROR":
			service = Service.objects.get(service_id=service_id)
			service.service_state = NextStateE2e[service.service_state].value
			service.save()

			update_service(service_id, {'service_state': service.service_state})

			if service.service_state != service.target_state:
				service = get_service(service_id)
				client = get_client(service['client_id'])

				generate_request = getattr(ServiceTypes[service['service_type']].value, "generate_" + service['service_type'] + "_request")
				request, service_state = generate_request(client, service, code="cpe")
				pprint(request)

		# Rollback all reservations if error
		# if service[0].service_state == "ERROR":
		# 	rollback_service(str(service_id))	

			response = { "message": "Service stated updated" }

		return JsonResponse(response, safe=False)


	def _existing_service(self, service_id):
	    return Service.objects.filter(service_id=service_id).count() is not 0


	def fetch_cpe(self, data, service, client, customer_location):
		client_node = get_client_node(service['client_node_sn'])
		"""
		Update Inventory with CPE data if needed
		"""
		if client_node['client'] is None:
			cpe_data = { 'client': client['name'], 'customer_location': customer_location['address'] }
			update_cpe(service['client_node_sn'], cpe_data)
	
		"""
		Get free CPE port from Inventory and
		mark it as a used port.
		"""
		cpe_port = get_free_cpe_port(service['client_node_sn'])
		cpe_port_id = cpe_port['id']

		#Assign CPE Port (mark as used)
		use_port(service['client_node_sn'], cpe_port_id)

		return cpe_port_id


class ProcessView(View):

	def post(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.get(service_id=service_id)

		if data['service_state'] != "ERROR":
			#move to the next state
			service.service_state = Fsm.to_next_state(service)
			service.save()

			if service.service_state != service.target_state:
				service.service_state = FSM.run(service)
			
			response = { "message": "Service stated updated" }

		
		else:
			response = { "message": "Service update failed" }
		return JsonResponse(response, safe=False)



