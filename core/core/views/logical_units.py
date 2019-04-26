from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests


class LogicalUnitsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def get(self, request):
        return _get_all_logicalunits()

    def post(self, request):
        body = json.loads(request.body.decode(encoding='UTF-8'))

        location = self._get_location(body['location_name'])
        router_node = self._get_router_node(location['id'])
               
        router_node_id = str(router_node['id'])

        free_logical_units = self._get_free_logical_units(router_node_id)

        free_logical_unit = free_logical_units[0]
        self._add_logical_unit_to_router_node(
            router_node_id, free_logical_unit['logical_unit_id'], body['product_id'])

        json_response = {
            "logical_unit_id": free_logical_unit['logical_unit_id']}

        return JsonResponse(json_response, safe=False)

    def _get_location(self, location_name):
        url = settings.INVENTORY_URL + "locations?name=" + location_name
        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response[0]
        else:
            return None

    def _get_router_node(self, location_id):
        url = settings.INVENTORY_URL + "locations/" + \
            str(location_id) + "/routernodes"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response[0]
        else:
            return None

    def _get_free_logical_units(self, router_node_id):
        url = settings.INVENTORY_URL + "routernodes/" + \
            str(router_node_id) + "/logicalunits?used=false"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)
        # TODO check minimum size = 2
        if json_response:
            return json_response
        else:
            return None

    def _add_logical_unit_to_router_node(self, router_node_id, logical_unit_id, product_id):
        url = settings.INVENTORY_URL + "routernodes/" + \
            str(router_node_id) + "/logicalunits"
        rheaders = {'Content-Type': 'application/json'}
        data = {"logical_unit_id": logical_unit_id, "product_id": product_id}
        response = requests.post(url, data=json.dumps(
            data), auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None


logical_units_view = LogicalUnitsView.as_view()
