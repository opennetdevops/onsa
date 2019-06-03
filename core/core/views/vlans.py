from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests


class VlansView(APIView):
    # swagger_schema = None # exclude from swagger schema
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def get(self, request, access_node_id):
        used = request.GET.get('used')
        free_vlan_tag = get_free_vlan_tag(access_node_id, used)

        json_response = {"vlan_tag": free_vlan_tag['vlan_tag']}

        return JsonResponse(json_response, safe=False)


vlans_view = VlansView.as_view()
