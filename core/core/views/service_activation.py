from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.constants import *
from core.views.ldap_jwt import *
from core.exceptions import *

import json
import requests
import logging


class ServiceActivationView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def post(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        if 'cpe_sn' in data.keys():
            if self.is_valid_cpe(data['cpe_sn']):
                service_data = {"client_node_sn": data['cpe_sn']}
                self.update_jeangrey_service(service_id, service_data)
            else:
                response = {"message": "CPE not valid."}
                return JsonResponse(response, safe=False)
        logging.debug(f'service activation with data: {data}')
        # For TIP service
        if 'vlan_id' in data.keys():
            logging.debug(f'TIP parameters: {data}')
            service_data = {"vlan_id": data['vlan_id']}
            self.update_jeangrey_service(service_id, service_data)
        else:
            logging.debug(f'not a tip')

        try:
            self.push_service_to_orchestrator(
                service_id, data['deployment_mode'], data['target_state'])
            service = get_service(service_id)
            return JsonResponse(service, safe=False)

        except ServiceException as e:
            e.handle()
        except BaseException as e:
            logging.error(e)
            msg = {MSG_HEADER: MSG_SERVICE_UPDATE_ERROR}
            return JsonResponse(msg, safe=False, status_code=HTTP_503_SERVICE_UNAVAILABLE)

    def is_valid_cpe(self, sn):
        cpe = get_cpe(sn)

        return True if cpe else False

    def update_jeangrey_service(self, service_id, data):
        url = settings.JEAN_GREY_URL + "services/" + str(service_id)
        rheaders = {'Content-Type': 'application/json'}
        response = requests.put(url, data=json.dumps(
            data), auth=None, verify=False, headers=rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None

    def push_service_to_orchestrator(self, service_id, deployment_mode, target_state):
        url = settings.CHARLES_URL + "services"

        rheaders = {'Content-Type': 'application/json'}
        data = {"service_id": service_id,
                "deployment_mode": deployment_mode, "target_state": target_state}
        r = requests.post(url, data=json.dumps(data), headers=rheaders)
        if r.status_code == HTTP_201_CREATED:
            return r.json()
        else:
            raise ServiceException("Unable to create service")


service_activation_view = ServiceActivationView.as_view()
