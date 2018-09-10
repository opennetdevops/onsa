from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
from enum import Enum
import json
import requests

from pprint import pprint

INVENTORY_URL = "http://127.0.0.1:8000/inventory/api/"
CHARLES_URL = "http://127.0.0.1:8000/charles/api/services"
BASE = "http://127.0.0.1:8000/"
CORE_URL = "http://127.0.0.1:8000/core/api/"

class PendingServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')

        if service_id is None:
            services_info = []

            s = Service.objects.all().values() if not state else Service.objects.filter(service_state=state).values()
            return JsonResponse(list(s), safe=False)

        else:
            s = Service.objects.filter(pk=service_id).values()[0]
            return JsonResponse(s, safe=False)

    #Pre: JSON with following format
    #{ 
    # cpe_sn: "",
    # service_id: 23
    # }
    #
    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        cpe_id = data['cpe_sn']
        vrf_name = data['vrf_name']

        service = Service.objects.get(id=data['service_id'])
        
        #Get CPE from inventory
        cpe_data = _get_cpe(cpe_id)

        #update inventory with Cpe Client
        if cpe_data is not None:
            cpe_data['client'] = service.client.name
            _update_cpe(cpe_id, cpe_data)
        else:
            response = {"message" : "Service - CPE relation POST failed"}
            return JsonResponse(response)

        #Create ports - and assign one
        cpe_port = _get_free_cpe_port(cpe_id)
        cpe_port_id = cpe_port['id']

        #Assign CPE Port (mark as used)
        _use_port(cpe_id, cpe_port_id)

        #update service
        service.client_node_sn = cpe_id
        service.vrf_name = vrf_name
        service.client_node_port = cpe_port['interface_name']

        r = _request_charles_service(service)

        if r.ok:
            service.service_state = "REQUESTED" #TODO use enum or similar but not hardcode
        else:
            service.service_state = "ERROR" #TODO use enum or similar but not hardcode

        service.save()
        response = {"message" : "Service - CPE relation requested"}
        
        return JsonResponse(response)




def _get_free_cpe_port(cpe_id):
    url= INVENTORY_URL + "clientnodes/" + cpe_id + "/clientports?used=False"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def _get_cpe(cpe_id):
    url= INVENTORY_URL + "clientnodes/" + cpe_id
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _update_cpe(cpe_id, data):
    url= INVENTORY_URL + "clientnodes/" + cpe_id
    rheaders = {'Content-Type': 'application/json'}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


def _get_service(service_id):
    url= CORE_URL + service_id
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def _request_charles_service(service):
    rheaders = {'Content-Type': 'application/json'}

    if service.vrf_name is not '':

        data = { 'data_model' : {
                                "service_id" : service.id,
                                "service_type" : service.service_type,
                                "client_id" : service.client.id,
                                "client_name" : service.client.name,
                                "location": service.location
                            },
                "vrf_name": service.vrf_name,
                "access_port_id": service.access_node_port,
                "access_node_id": service.access_node,
                "prefix" : service.prefix,
                "client_node_port" : service.client_node_port,
                "client_node_sn" : service.client_node_sn,
                "bandwidth" : service.bandwidth
        }
    else:
            data = { 'data_model' : {
                            "service_id" : service.id,
                            "service_type" : service.service_type,
                            "client_id" : service.client.id,
                            "client_name" : service.client.name,
                            "location": service.location
                        },
            "access_port_id": service.access_node_port,
            "access_node_id": service.access_node,
            "prefix" : service.prefix,
            "client_node_port" : service.client_node_port,
            "client_node_sn" : service.client_node_sn,
            "bandwidth" : service.bandwidth
        }

    pprint(data)

    r = requests.post(CHARLES_URL, data = json.dumps(data), headers=rheaders)
    print("r:", r)
    return r

def _use_port(client_node_id, client_port_id):
    url= INVENTORY_URL + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    print(response.text)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None



