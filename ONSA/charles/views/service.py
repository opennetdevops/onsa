from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from charles.models import Service
from charles.services import ServiceHandler
from enum import Enum
from pprint import pprint
import requests
import json

class ServiceStatuses(Enum):
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

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
		service = self.get_service(service_id)
		client = self.get_client(service['client_id'])
		
		client_node_sn = service['client_node_sn']

		"""
		Update Inventory with CPE data
		"""
		cpe_data = { 'client': client['name'] }
		self.update_cpe(client_node_sn, cpe_data)
	
		"""
		Get free CPE port from Inventory and
		mark it as a used port.
		"""
		cpe_port = self.get_free_cpe_port(client_node_sn)
		cpe_port_id = cpe_port['id']
		client_node_port = cpe_port['interface_name']


		#Assign CPE Port (mark as used)
		self.use_port(client_node_sn, cpe_port_id)

		#Check if exists (retry support)
		if not self.existing_service(service_id):
			service = Service.objects.create(service_id=service_id, service_state=service['service_state'] )

		# Save locally
		service = Service.objects.get(service_id=service_id)
		service.service_state = ServiceStatuses['REQUESTED'].value
		service.save()

		#Update JeanGrey
		service_data = { "client_port_id": cpe_port_id, "service_state": ServiceStatuses['REQUESTED'].value}
		self.update_service(service_id, service_data)

		#Trigger Worker
		generate_request = getattr(ServiceHandler.ServiceHandler, "generate_" + service.service_type + "_request")
		generate_request(data)
		
		
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
			self.rollback_service(str(service_id))

		self.update_core_service_status(str(service_id), data)

		return HttpResponse(data, content_type='application/json')

	def _assign_autonomous_system(self, vrf_name):    
		list_as = list( Service.objects.filter(vrf_name=vrf_name).values('autonomous_system') )
		print("list_as",list_as)
		
		if (len(list_as) == 1) and (list_as[0]['autonomous_system'] is 0):
			return 65000

		ordered_list_as = sorted(list_as, key=lambda k: k['autonomous_system'])
		last_as = int( ordered_list_as[-1]['autonomous_system'] )

		if last_as <= 65500:
			return (last_as + 1)
		else:
			while(1):
				proposed_as = 65000
				if proposed_as > 65500:
					#TODO throw exception
					return -1

				if Service.objects.filter(vrf_name=vrf_name, autonomous_system=proposed_as).values().count():
					proposed_as+=1
				else:
					return proposed_as

	def _get_vrf(self, vrf_id):
		url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id)
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def existing_service(self, service_id):
		return Service.objects.filter(service_id=service_id).count() is not 0

	def rollback_service(self, service_id):
		url = "/api/products/" + service_id + "/rollback"
		r = requests.post(url)

	def update_core_service_status(self, service_id, data):
		rheaders = {'Content-Type': 'application/json'}
		url = settings.CORE_URL +"services/" + service_id
		r = requests.put(url, data = json.dumps(data), headers=rheaders)

	def get_free_cpe_port(self, client_node_sn):
		url= settings.INVENTORY_URL + "clientnodes/" + client_node_sn + "/clientports?used=False"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def update_cpe(self, client_node_sn, data):
		url = settings.INVENTORY_URL + "clientnodes/" + client_node_sn
		rheaders = {'Content-Type': 'application/json'}
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def get_service(self, service_id):
		url = settings.JEAN_GREY_URL + "services/" + service_id
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def get_client(self, client_id):
		url = settings.JEAN_GREY_URL + "clients/"  + str(client_id)
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def use_port(self, client_node_id, client_port_id):
		url= settings.INVENTORY_URL + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)

		rheaders = { 'Content-Type': 'application/json' }
		data = { "used": True }
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

	def update_service(self, service_id, data):
		url = settings.JEAN_GREY_URL + "services/" + service_id
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None
