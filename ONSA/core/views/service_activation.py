from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from enum import Enum
import json
import requests
import logging
import coloredlogs
from pprint import pprint

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
AS_SERVICES = ['cpe_mpls']
CLIENT_NETWORK_SERVICES = ['cpeless_mpls']
PREFIX_SERVICES = ['cpeless_irs', 'vcpe_irs', 'cpeless_mpls']

coloredlogs.install()

class ServiceActivationView(View):
	
	def post(self, request, service_id):
		logging.basicConfig(level=logging.INFO)

		data = json.loads(request.body.decode(encoding='UTF-8'))
		print(data)
		
		if 'cpe_sn' in data.keys():
			if self.is_valid_cpe(data['cpe_sn']):
				service_data = { "client_node_sn": data['cpe_sn']}
				self.update_service(service_id, service_data)
			else:
				response = { "message" : "CPE not valid." }
				return JsonResponse(response, safe=False)

		r = self.push_service_to_orchestrator(service_id)
		return JsonResponse(r.status_code, safe=False)

	def is_valid_cpe(self, sn):
		cpe = self._get_cpe(sn)

		return True if cpe else False
	
	def _get_cpe(self, sn):
		url = settings.INVENTORY_URL + "clientnodes/" + str(sn)
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None	

	def update_service(self, service_id, data):
		url = settings.JEAN_GREY_URL + "services/" + str(service_id)
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def push_service_to_orchestrator(self, service_id):
		url = settings.CHARLES_URL + "services"

		rheaders = { 'Content-Type': 'application/json' }	
		data = { "service_id": service_id }	
		r = requests.post(url, data = json.dumps(data), headers = rheaders)
		return r