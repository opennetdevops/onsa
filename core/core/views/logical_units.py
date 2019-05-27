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
        # return JsonResponse(get_all_logicalunits(), safe=False) 
        # TODO: not implemented
        pass

    def post(self, request):
        body = json.loads(request.body.decode(encoding='UTF-8'))

        router_node = get_router_node(body['location_id'])
        router_node_id = str(router_node['id'])

        free_logical_units = get_free_logical_units(router_node_id)

        free_logical_unit = free_logical_units[0]
        add_logical_unit_to_router_node(
            router_node_id, free_logical_unit['logical_unit_id'], body['product_id'])

        json_response = {
            "logical_unit_id": free_logical_unit['logical_unit_id']}

        return JsonResponse(json_response, safe=False)


logical_units_view = LogicalUnitsView.as_view()
