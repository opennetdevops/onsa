from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests

from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.utils import no_body, swagger_auto_schema

class ClientView(APIView):
    '''
    get:
    List of clients serialized to JSON.

    post:
    Creates a new client.
    '''

    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def get(self, request, client_id=None):
        url = settings.JEAN_GREY_URL + "clients"
        name = request.GET.get('name', None)
        search = request.GET.get('search', None)


        if client_id is not None:
            url += "/" + str(client_id)
        elif name is not None:
            url += "?name=" + name
        elif search is not None:
            url += "?search=" + search    

        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False, status=response.status_code)

    # Decorator for SWAGGER, allows to create custom attributes
    @swagger_auto_schema(
    # operation_description="apiview post description override",
      request_body=openapi.Schema(
          type=openapi.TYPE_OBJECT,
          required=['name'],
          properties={
              'name': openapi.Schema(type=openapi.TYPE_STRING)
          },
      ),
      tags=['clients'],
    )
    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        url = settings.JEAN_GREY_URL + "clients"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(
            data), auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False, status=response.status_code)


client_view = ClientView.as_view()
