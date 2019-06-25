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
        access_port_id = request.GET.get('access_port_id', None)


        if service_id is not None:
            url = settings.JEAN_GREY_URL + "services/"+ str(service_id)
        else:
            url = settings.JEAN_GREY_URL + "services"
            if state is not None:
                url += "?state=" + state
            elif service_type is not None:
                url += "?type=" + service_type
            elif access_port_id is not None:
                url += "?access_port_id=" + access_port_id

        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        # json_response = json.loads(response.text) # ToDo - try to user r.json

        #return JsonResponse(json_response, safe=False)
        return JsonResponse(response.json(), safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        url = settings.JEAN_GREY_URL + "services"
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
        return JsonResponse(response.json(), safe=False, status=response.status_code)     

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        url = settings.JEAN_GREY_URL + "services/" + str(service_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        return JsonResponse(json_response, safe=False)
        
    def delete(self, request, service_id):
        service = get_service(service_id)
        
        if service['service_state'] == INITIAL_SERVICE_STATE:
            status = delete_jeangrey_service(service_id)
        else:
            status = delete_charles_service(service_id)

        if status == HTTP_204_NO_CONTENT:
            data = {"msg" : "Service deleted successfully"}
        else:
            data = {"msg" : "Unable to delete service"}
            status = ERR_SERVICE_UNABLETODELETE
        return JsonResponse(data, safe=False, status=HTTP_200_OK)
    
service_view = ServiceView.as_view()