from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests

class VrfsView(APIView):
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
		vrf = {"vrf_id":vrf_id}
		self._add_vrf_to_location(location['id'])
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

	def _add_vrf_to_location(self, location_id, data):
	    url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id) + "/vrfs"
	    rheaders = { 'Content-Type': 'application/json' }
	    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
	    if response.status_code == HTTP_201_CREATED:
	        return response.json()
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

vrfs_view = VrfsView.as_view()
