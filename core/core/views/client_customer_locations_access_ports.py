from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests


class ClientCustomerLocationAccessPortsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def get(self, request, client_id, customer_location_id):
        url = settings.JEAN_GREY_URL + "clients/" + \
            str(client_id) + "/customerlocations/" + \
            str(customer_location_id) + "/accessports"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


client_customer_location_access_ports_view = ClientCustomerLocationAccessPortsView.as_view()
