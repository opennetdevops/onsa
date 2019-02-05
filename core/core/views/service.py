from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests

class ServiceView(APIView):

    authentication_classes = ([JSONWebTokenLDAPAuthentication,])
    permission_classes = (IsAuthenticated,)

    def get(self, request, service_id=None):

        state = request.GET.get('state', None)
        service_type = request.GET.get('type', None)

        if service_id is not None:
            url = settings.JEAN_GREY_URL + "services/"+ str(service_id)
        else:
            url = settings.JEAN_GREY_URL + "services"
            if state is not None:
                url += "?state=" + state
            elif service_type is not None:
                url += "?type=" + service_type

        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        url = settings.JEAN_GREY_URL + "services"
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)     

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        url = settings.JEAN_GREY_URL + "services/" + str(service_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)
    def delete(self, request, service_id):
        delete_jeangrey_service(service_id)
        delete_charles_service(service_id)
        data = {"Message" : "Service deleted successfully"}

        return JsonResponse(data)
    
service_view = ServiceView.as_view()