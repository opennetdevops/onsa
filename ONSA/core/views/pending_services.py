from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, ServiceCpeRelations
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

            s = ServiceCpeRelations.objects.all() if not state else ServiceCpeRelations.objects.filter(service__service_state=state)

            for relation in s:
                info = { 'client_name' : relation.service.client.name,
                                     'client_node_sn' : relation.cpe_port.cpe.serial_number,
                                     'client_node_port' : relation.cpe_port.name,
                                     'bandwidth' : relation.service.bandwidth,
                                     'prefix' : relation.service.prefix,
                                     'vrf' : relation.service.vrf,
                                     'service_state' : relation.service.service_state,
                                     'product_identifier' : relation.service.product_identifier,
                                     'service_type' : relation.service.service_type,
                                     'service_id' : relation.service.id }

                services_info.append(info)

            return JsonResponse(services_info, safe=False)

        else:
            s = ServiceCpeRelations.objects.get(service__pk=service_id)

            service_info = { 'client_name' : s.service.client.name,
                             'client_node_sn' : s.cpe_port.cpe.serial_number,
                             'client_node_port' : s.cpe_port.name,
                             'bandwidth' : s.service.bandwidth,
                             'prefix' : s.service.prefix,
                             'vrf' : s.service.vrf,
                             'service_state' : s.service.service_state,
                             'product_identifier' : s.service.product_identifier,
                             'service_type' : s.service.service_type }

            return JsonResponse(service_info, safe=False)

    #Pre: JSON with following format
    #{ 
    # cpe_sn: "",
    # service_id: 23
    # }
    #
    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        
        #Get CPE from inventory
        cpe_port = _get_free_cpe_port(data['cpe_sn'])
        cpe_port_id = cpe_port['id']

        service_relation = ServiceCpeRelations(cpe_port=cpe_port_id,service=data['service_id'])
        service_relation.save()

        service = _get_service(data['service_id'])

        r = _request_charles_service(service_relation)

        if r.ok:
            service.service_state = "REQUESTED" #TODO use enum or similar but not hardcode
        else:
            service.service_state = "ERROR" #TODO use enum or similar but not hardcode

        service.save()
        response = {"message" : "Service - CPE relation requested"}
        
        return JsonResponse(response)



    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.objects.filter(pk=service_id)
        service_relation = ServiceCpeRelations.objects.filter(service__pk=service_id)
        service_relation.update(**data)
        service.update(**data)

        return JsonResponse(data, safe=False)

def _get_free_cpe_port(cpe_id):
    url= INVENTORY_URL + "clientnodes/" + cpe_id + "/clientports/?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
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

def _request_charles_service(service_relation):
        data = { 'data_model' : {
                                "service_id" : service_relation['service'],
                                "service_type" : service_relation['service'].service_type,
                                "client_id" : service_relation['service'].client,
                                "client_name" : service_relation['service'].client.name,
                                "location": service_relation['service'].location
                            },
                "prefix" : service_relation['service'].prefix,
                "client_node_port" : service_relation['cpe_port'],
                "client_node_sn" : service_relation['cpe_port'].cpe.serial_number,
                "bandwidth" : service_relation['service'].bandwidth
        }

        pprint(data)

        r = requests.post(CHARLES_URL, data = json.dumps(data), headers=rheaders)
        return r





