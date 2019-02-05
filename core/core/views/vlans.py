from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests

class VlansView(APIView):

	def get(self, request, access_node_id):
		used = request.GET.get('used')
		free_vlan_tag = self._get_free_vlan_tag(access_node_id, used)

		json_response = {"vlan_tag": free_vlan_tag['vlan_tag']}

		return JsonResponse(json_response, safe=False)

	def _get_free_vlan_tag(self, access_node_id, used):
		url = settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags?used=" + used
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)
		if json_response:
			return json_response[0]
		else:
			return None

vlans_view = VlansView.as_view()
