from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
import requests

class VlansView(View):

	def get(self, request, access_node_id):
		used = request.GET.get('used')
		free_vlan_tag = self._get_free_vlan_tag(access_node_id, used)

		json_response = {"vlan_tag": free_vlan_tag['vlan_tag']}

		return JsonResponse(json_response, safe=False)

	def post(self, request):
		pass

	def put(self, request):
		pass

	def delete(self, request):
		pass

	def _get_free_vlan_tag(self, access_node_id, used):
		url = settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags?used=" + used
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None


class LogicalUnitsView(View):
	def get(self, request):
	   return _get_all_logicalunits()

	def post(self, request):
		body = json.loads(request.body.decode(encoding='UTF-8'))

		location = self._get_location(body['location_name'])
		router_node = self._get_router_node(location['id'])
		router_node_id = str(router_node['id'])

		free_logical_units = self._get_free_logical_units(router_node_id)

		free_logical_unit = free_logical_units[0]
		self._add_logical_unit_to_router_node(router_node_id, free_logical_unit['logical_unit_id'], body['product_id'])

		json_response = { "logical_unit_id": free_logical_unit['logical_unit_id'] }

		return JsonResponse(json_response, safe=False)
		

	def put(self, request):
		pass

	def delete(self, request):
		pass

	def _get_all_logical_units(self):
		pass

	def _get_location(self, location_name):
		url = settings.INVENTORY_URL + "locations?name="+ location_name
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
		    return json_response[0]
		else:
		    return None

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

	def _add_logical_unit_to_router_node(self, router_node_id,logical_unit_id, product_id):
		url = settings.INVENTORY_URL + "routernodes/" + str(router_node_id) + "/logicalunits"
		rheaders = {'Content-Type': 'application/json'}
		data = {"logical_unit_id":logical_unit_id, "product_id": product_id}
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
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


class CustomerLocationsView(View):
	def get(self, request, client_id):
		url = settings.JEAN_GREY_URL + "clients/" + str(client_id) + "/customerlocations"

		rheaders = {'Content-Type': 'application/json'}	
		response = requests.get(url, auth = None, verify = False, headers = rheaders)

		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

	def post(self, request):
		pass

class VrfsView(View):
	def get(self, request):
		client = request.GET.get('client')
		url = settings.INVENTORY_URL + "vrfs"

		if client is not None:
			url += "?client=" + client

		rheaders = {'Content-Type': 'application/json'}	
		response = requests.get(url, auth = None, verify = False, headers = rheaders)

		json_response = json.loads(response.text)

		json_response = {'count': len(json_response), 'vrfs': json_response}

		return JsonResponse(json_response, safe=False)

	def post(self, request):
		pass

	def put(self, request):
		body = json.loads(request.body.decode(encoding='UTF-8'))

		client = body['client']
		name = body['name']
		description = body['description']
		product_id = body['product_id']

		location = self._get_location(body['location_name'])

		vrf = self._request_vrf()
		vrf_id = vrf['rt']

		self._update_vrf(vrf_id, client, name, description)
		self._add_location_to_vrf(vrf_id, location['id'])
		self._attach_vrf_to_product(vrf_id, product_id)

		json_response = {"vrf_id" : str(vrf_id)}

		return JsonResponse(json_response, safe=False)

	def delete(self, request):
		pass

	def _request_vrf(self):
		url = settings.INVENTORY_URL + "vrfs?used=False"
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)[0]

		if json_response:
			return json_response
		else:
			return None

	def _update_vrf(self, vrf_id, client, name, description):
		url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id)
		rheaders = {'Content-Type': 'application/json'}		
		data = { "client": client,
			     "name": name,
			     "description": description,
			     "used": True }

		print(data)

		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		if json_response:
			return json_response
		else:
			return None

	def _get_location(self, location):
		url = settings.INVENTORY_URL + "locations?name="+ location
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

	def _add_location_to_vrf(self, vrf_id, location_id):
		url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id) + "/locations/" + str(location_id)
		rheaders = {'Content-Type': 'application/json'}		
		response = requests.put(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		if json_response:
			return json_response
		else:
			return None
	
	def _attach_vrf_to_product(self, vrf_id, product_id):	
		url = settings.INVENTORY_URL + "products/" + str(product_id)
		data = {"vrf_id": vrf_id }
		rheaders = {'Content-Type': 'application/json'}		
		response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		if json_response:
			return json_response
		else:
			return None


class ClientView(View):
	def get(self, request, client_id=None):

		url = settings.JEAN_GREY_URL + "clients"
		name = request.GET.get('name', None)

		if client_id is not None:
			url += "/" + str(client_id)
		elif name is not None:
			url += "?name=" + name		
		
		rheaders = { 'Content-Type': 'application/json' }		
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		
		return JsonResponse(json_response, safe=False)

		
	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		url = settings.JEAN_GREY_URL + "clients"
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

	def put(self, request):
		pass

	def delete(self, request):
		pass


class ClientAccessPortsView(View):
	def get(self, request, client_id):
		pass
		
	def post(self, request):
		pass

	def put(self, request):
		pass

	def delete(self, request):
		pass	