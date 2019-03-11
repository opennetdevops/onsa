from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests


class ClientView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def get(self, request, client_id=None):

        url = settings.JEAN_GREY_URL + "clients"
        name = request.GET.get('name', None)

        if client_id is not None:
            url += "/" + str(client_id)
        elif name is not None:
            url += "?name=" + name

        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        url = settings.JEAN_GREY_URL + "clients"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(
            data), auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)


client_view = ClientView.as_view()
