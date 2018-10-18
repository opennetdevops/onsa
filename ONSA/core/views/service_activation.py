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
		client_node_sn = data['cpe_sn']

		"""
		Get service and client info from Service Inventory
		"""	
		logging.info("Fetching service and client data.")
		service = _get_service(service_id)
		client = _get_client(service['client_id'])
		
		"""
		Get CPE info from Inventory
		"""		
		cpe = _get_cpe(client_node_sn) 

		
		"""
		Update Inventory with CPE data
		"""
		logging.info("Updating CPE info in inventory.")
		if cpe is not None:
			cpe['client'] = client['name']
			_update_cpe(client_node_sn, cpe)
		else:
			logging.error("Service activation failed. REASON: CPE does not exist.")
			response = { "message" : "Service activation failed. REASON: CPE does not exist." }
			return JsonResponse(response)

		"""
		Get free CPE port from Inventory and
		mark it as a used port.
		"""
		logging.info("Fetching free CPE port.")
		cpe_port = _get_free_cpe_port(client_node_sn)
		cpe_port_id = cpe_port['id']
		client_node_port = cpe_port['interface_name']


		#Assign CPE Port (mark as used)
		_use_port(client_node_sn, cpe_port_id)

		data = _generate_json_data(service)

		_update_service(service_id, data)

		# r = _request_charles_service(data)

		# if r.ok:
		# 	data = { 'service_state': 'REQUESTED'}
		# 	_update_service(service_id, data) #TODO use enum or similar but not hardcode
		# else:
		# 	data = { 'service_state': 'ERROR'}
		# 	_update_service(service_id, data) #TODO use enum or similar but not hardcode

		response = {"message" : "Service - CPE relation requested"}
		
		return JsonResponse(response)
		
def _get_free_cpe_port(client_node_sn):
	url= settings.INVENTORY_URL + "clientnodes/" + client_node_sn + "/clientports?used=False"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None

def _get_cpe(client_node_sn):
	url= settings.INVENTORY_URL + "clientnodes/" + client_node_sn
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def _update_cpe(client_node_sn, data):
	url = settings.INVENTORY_URL + "clientnodes/" + client_node_sn
	rheaders = {'Content-Type': 'application/json'}
	response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None


def _update_service(service_id, data):
	url = settings.JEAN_GREY_URL + "services/" + service_id
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def _get_service(service_id):
	url = settings.JEAN_GREY_URL + "services/" + service_id
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def _get_client(client_id):
	url = settings.JEAN_GREY_URL + "clients/"  + str(client_id)
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def _generate_service_inventory_json(service, client):



	return data

def _generate_json_data(service, client, client_node_port):

	bandwidth = service['bandwidth']
	access_node_id = service['access_node_id']
	access_port_id = service['access_port_id']
	client_node_sn = service['client_node_sn']
	location = _get_location(service['location_id'])

	service_type = service['service_type']

	data = { 'data_model' : {
						"service_id" : service['id'],
						"service_type" : service['service_type'],
						"client_id" : service['client_id'],
						"client_name" : client['name'],
						"location": location['name']
					},

			"access_port_id": access_port_id,
			"access_node_id": access_node_id,
			"client_node_port" : client_node_port,
			"client_node_sn" : client_node_sn,
			"bandwidth" : bandwidth
	}
	
	if service_type in CLIENT_NETWORK_SERVICES:        
		data["client_network"] = service['client_network']

	if service_type in PREFIX_SERVICES:
		data["prefix"] = service['prefix']

	if service_type in VRF_SERVICES:
		vrf = _get_vrf(service['vrf_id'])
		vrf_name = vrf['name']
		data['vrf_name'] = vrf_name

		if service_type in AS_SERVICES:
			autonomous_system = _assign_autonomous_system(vrf_name)
			data['client_as']  =  autonomous_system 

	return data


def _request_charles_service(data):
	rheaders = { 'Content-Type': 'application/json' }
	url = settings.CHARLES_URL + "services"
	r = requests.post(url, data = json.dumps(data), headers=rheaders)
	print("r:", r)
	return r

def _use_port(client_node_id, client_port_id):
	url= settings.INVENTORY_URL + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)

	rheaders = { 'Content-Type': 'application/json' }
	data = { "used": True }
	response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	print(response.text)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def _assign_autonomous_system(vrf_name):    
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


def _get_access_node(access_node_id):
	url = settings.INVENTORY_URL + "accessnodes/" + str(access_node_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None


def _get_vrf(vrf_id):
	url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None


def _get_location(location_id):
	url = settings.INVENTORY_URL + "locations/" + str(location_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None