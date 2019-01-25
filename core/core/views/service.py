from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from enum import Enum
import json
import requests
from core.utils.utils import *
import os

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
IRS_SERVICES = ['cpeless_irs', 'cpe_irs', 'vcpe_irs']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']

BB_STATES = ['bb_data_ack', 'bb_activated', 'bb_activation_in_progress']
CPE_STATES = ['cpe_data_ack', 'cpe_activation_in_progress', 'service_activated']
AN_STATES = ['an_data_ack', 'an_activation_in_progress']


def delete_charles_service(service_id):
    url = os.getenv('CHARLES_URL') + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def delete_jeangrey_service(service_id):
    url = os.getenv('JEAN_GREY_URL') + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', None)
        service_type = request.GET.get('type', None)

        if service_id is not None:
            url = os.getenv('JEAN_GREY_URL') + "services/"+ str(service_id)
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

        url = os.getenv('JEAN_GREY_URL') + "services"
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        url = os.getenv('JEAN_GREY_URL') + "services/" + str(service_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)
    def delete(self, request, service_id):
        delete_jeangrey_service(service_id)
        delete_charles_service(service_id)
        data = {"Message" : "Service deleted successfully"}
        return JsonResponse(data)

class ServiceResourcesView(View):
    def get(self, request, service_id=None):

        if service_id is not None:
            service = get_service(service_id)
            json_response = self.get_resources(service)

        return JsonResponse(json_response, safe=False)


    def get_resources(self, service):

        service = pop_empty_keys(service)

        router_node = get_router_node(service['router_node_id'])
        access_node = get_access_node(service['access_node_id'])
        access_port = get_access_port(service['access_port_id'])
        location = get_location(service['location_id'])
        customer_location = get_customer_location(service['client_id'], service['customer_location_id'])
        client = get_client(service['client_id'])
       

        resources = { 
                      "customer" : client['name'],
                      "location": location['name'],
                      "customer_location": customer_location['address'],
                      "router_node": { 'name': router_node['name'] },
                      "access_node": { "model": access_node['model'],
                                       "name": access_node['name'],
                                       "access_port": access_port['port'] },
                      "vlan_id": service['vlan_id'],
                    }

        if service['service_type'] in VRF_SERVICES:
            resources['client_network'] = service['client_network']
        elif service['service_type'] in IRS_SERVICES:
            if 'public_network' in service.keys():
                resources['public_network'] = service['public_network']

        if service['service_state'] in BB_STATES:
            resources['router_node']['logical_unit_id'] = service['logical_unit_id']
            if service['service_type'] == "vcpe_irs":
                resources['router_node']['vcpe_logical_unit_id'] = service['vcpe_logical_unit_id']
        elif service['service_state'] in CPE_STATES:     
            client_node = get_client_node(service['client_node_sn'])

            resources["client_node"] = { "model": client_node['model'],
                                         "wan_port": client_node['uplink_port'],
                                         "SN": client_node['serial_number'] }

            if 'client_port_id' in service.keys():
                client_port = get_client_port(service['client_node_sn'], service['client_port_id'])
                resources['client_node']['client_port'] = client_port['interface_name']           


             
 
        
        return resources


