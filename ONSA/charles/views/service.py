from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from charles.models import Service
from charles.services import cpeless_irs_service, cpe_mpls_service, cpeless_mpls_service, vcpe_irs_service
from charles.services import vpls_service
from enum import Enum
from charles.utils.utils import *
from pprint import pprint
import requests
import json

class ServiceStatuses(Enum):
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class ServiceTypes(Enum):
    cpeless_irs = cpeless_irs_service
    cpe_mpls = cpe_mpls_service
    cpeless_mpls = cpeless_mpls_service
    vcpe_irs = vcpe_irs_service
    vpls = vpls_service


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
		service_id = data['service_id']

		"""
		Get service and client info from Service Inventory
		"""	
		service = get_service(service_id)
		client = get_client(service['client_id'])
		
		client_node_sn = service['client_node_sn']

		"""
		Update Inventory with CPE data
		"""
		cpe_data = { 'client': client['name'] }
		update_cpe(client_node_sn, cpe_data)
	
		"""
		Get free CPE port from Inventory and
		mark it as a used port.
		"""
		cpe_port = get_free_cpe_port(client_node_sn)
		cpe_port_id = cpe_port['id']
		client_node_port = cpe_port['interface_name']


		#Assign CPE Port (mark as used)
		use_port(client_node_sn, cpe_port_id)

		#Check if exists (retry support)
		if not self._existing_service(service_id):
			service = Service.objects.create(service_id=service_id, service_state=service['service_state'] )

		# Save locally
		service = Service.objects.get(service_id=service_id)
		service.service_state = ServiceStatuses['REQUESTED'].value
		service.save()

		#Update JeanGrey
		service_data = { "client_port_id": cpe_port_id, "service_state": ServiceStatuses['REQUESTED'].value}
		update_service(service_id, service_data)

		#Get Service from JeanGrey
		service = get_service(service_id)

		#Trigger Worker
		generate_request = getattr(ServiceTypes[service['service_type']].value, "generate_" + service['service_type'] + "_request")
		generate_request(client, service)
		
		
		response = { "message": "Service Requested." }
		return JsonResponse(response)

	def put(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.filter(service_id=service_id)
		service.update(**data)
		data = serializers.serialize('json', service)

		#Update service status in core
		data = {
			"service_state":service[0].service_state
		}

		#Rollback all reservations if error
		if service[0].service_state == ServiceStatuses['ERROR'].value:
			rollback_service(str(service_id))

		update_core_service_status(str(service_id), data)

		return HttpResponse(data, content_type='application/json')


	def _existing_service(self, service_id):
	    return Service.objects.filter(service_id=service_id).count() is not 0
