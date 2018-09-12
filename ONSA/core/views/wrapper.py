from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.views import View
import json
import requests

class VlansView(View):

	def get(self, request):
		pass

	def post(self, request):
		body = json.loads(request.body.decode(encoding='UTF-8'))
		#
		# TODO!!! INCLUDE LOCATION 
		# 
		#
		# TODO!!! INCLUDE LOCATION 
		# 
		#
		# TODO!!! INCLUDE LOCATION 
		# 
		#
		# TODO!!! INCLUDE LOCATION 
		# 
		free_vlan_tag = self._get_free_vlan_tag(body['access_port_id'])
		access_port = self._get_port(body['access_port_id'])
		self._add_vlan_tag_to_access_node(access_port['accessNode_id'], access_port['id'], free_vlan_tag['vlan_tag'], )

		json_response = { 'vlan_tag': free_vlan_tag['vlan_tag'] }

		return JsonResponse(json_response, safe=False)


	def put(self, request):
		pass

	def delete(self, request):
		pass

	def _get_free_vlan_tag(self, access_port_id):
		url = settings.INVENTORY_URL + "accessnodes/"+ str(access_port_id) + "/vlantags?used=false"
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_port(self, access_port_id):
		url = settings.INVENTORY_URL + "accessports/" + str(access_port_id)
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		if json_response:
			return json_response
		else:
			return None

	def _add_vlan_tag_to_access_node(self, access_node_id, access_port_id, vlan_tag):
		url= settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags"
		rheaders = { 'Content-Type': 'application/json' }
		data = {"vlan_tag": vlan_tag,
				"service_id": None,
				"client_node_sn": None,
				"client_node_port": None,
				"bandwidth": None,
				"access_port_id": access_port_id}
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

class LogicalUnitsView(View):
	def get(self, request):
	   pass

	def post(self, request):
		body = json.loads(request.body.decode(encoding='UTF-8'))

		router_node = self._get_router_node(body['location_id'])
		router_node_id = str(router_node['id'])

		free_logical_units = self._get_free_logical_units(router_node_id)

		free_logical_unit = free_logical_units[0]
		self._add_logical_unit_to_router_node(router_node_id, free_logical_unit['logical_unit_id'])

		json_response = { "logical_unit_id": free_logical_unit['logical_unit_id'] }

		return JsonResponse(json_response, safe=False)
		

	def put(self, request):
		pass

	def delete(self, request):
		pass

	def _get_router_node(self, location_id):
		url= settings.INVENTORY_URL + "locations/" + str(location_id) + "/routernodes"
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _get_free_logical_units(self, router_node_id):
		url = settings.INVENTORY_URL + "routernodes/" + str(router_node_id) + "/logicalunits?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		#TODO check minimum size = 2
		if json_response:
			return json_response
		else:
			return None

	def _add_logical_unit_to_router_node(self, router_node_id,logical_unit_id):
		url = settings.INVENTORY_URL + "routernodes/" + str(router_node_id) + "/logicalunits"
		rheaders = {'Content-Type': 'application/json'}
		data = {"logical_unit_id":logical_unit_id}
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response
		else:
			return None

class IpamView(View):
	def get(self, request):
	   pass

	def post(self, request):
		token = self._get_ipam_authentication_token()

		network = self._get_network("") # ToDo: inputs

		json_response = {} # ToDo

		return JsonResponse(json_response, safe=False)

	def put(self, request):
		pass

	def delete(self, request):
		pass

	def _get_ipam_authentication_token(self):
		url = settings.IPAM_URL + "/api/authenticate"
		rheaders = { 'Content-Type': 'application/json' }
		
		#App User
		data = { "email": "malvarez@lab.fibercorp.com.ar", "password": "Matias.2015" }
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		return json.loads(response.text)['auth_token']

	def _get_network(self, prefix, description, ip_version):
		owner = "Proyectos"
		token = self._get_ipam_authentication_token()

		url = settings.IPAM_URL + "/api/networks/assign_subnet"

		rheaders = {
					 'Content-Type': 'application/json',
			  	     'Authorization': 'Bearer ' + token
			  	   }
		data = { 
				 "description": description,
				 "owner": owner,
				 "ip_version": ip_version,
				 "mask": prefix
			   }

		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		
		if "network" in json_response:
			return json_response["network"]
		else:
			return None

class AccessPortsView(View):
	def get(self, request):
	   pass

	def post(self, request):
		body = json.loads(request.body.decode(encoding='UTF-8'))
		"""
		Fetch one access port in a given location.
		"""
		free_access_port = self._get_free_access_port(body['location_id'])
		access_port_id = str(free_access_port['id'])

		"""
		Reserve previously fetched access port.
		"""
		self._use_port(access_port_id)

		"""
		Fetch reserved access port information.
		"""
		json_response = self._get_port(access_port_id)

		return JsonResponse(json_response, safe=False)
		

	def put(self, request):
		pass

	def delete(self, request):
		pass

	def _get_free_access_port(self, location_id):
		url = settings.INVENTORY_URL + "locations/"+ str(location_id) + "/accessports?used=false"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _use_port(self, access_port_id):
		url = settings.INVENTORY_URL + "accessports/" + access_port_id
		rheaders = {'Content-Type': 'application/json'}
		data = { "used": True }
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		if json_response:
			return json_response
		else:
			return None

	def _get_port(self, access_port_id):
		url = settings.INVENTORY_URL + "accessports/" + access_port_id
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		if json_response:
			return json_response
		else:
			return None

class LocationsView(View):
	def get(self, request):
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(settings.INVENTORY_URL + "locations", auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

	def post(self, request):
		pass

	def put(self, request):
		pass

	def delete(self, request):
		pass


class VrfsView(View):
	def get(self, request):
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(settings.INVENTORY_URL + "vrfs", auth = None, verify = False, headers = rheaders)

		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

	def post(self, request):
		pass

	def put(self, request):
		pass

	def delete(self, request):
		pass