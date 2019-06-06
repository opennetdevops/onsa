from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests

from drf_yasg.utils import no_body, swagger_auto_schema

class CustomerLocationsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    @swagger_auto_schema(tags=['customerlocations'])
    def get(self, request, client_id, customer_location_id=None):
        url = settings.JEAN_GREY_URL + "clients/" + \
            str(client_id) + "/customerlocations"

        if customer_location_id is not None:
            url += "/" + str(customer_location_id)

        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)

        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)
        
    @swagger_auto_schema(tags=['customerlocations'])
    def post(self, request, client_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        url = settings.JEAN_GREY_URL + "clients/" + \
            str(client_id) + "/customerlocations"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(
            data), auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False, status=response.status_code)


customer_locations_view = CustomerLocationsView.as_view()
