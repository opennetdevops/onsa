from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from jeangrey.models import Client, Service
from jeangrey import models
from enum import Enum
import json
import requests
from pprint import pprint

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']
PROJECT_SERVICES = ['projects']


class ServiceTypes(Enum):
    cpeless_irs = "CpelessIrs"
    cpe_irs = "CpeIrs"
    cpeless_mpls = "CpelessMpls"
    cpe_mpls = "CpeMpls"
    vcpe_irs = "VcpeIrs"
    vpls = "Vpls"

class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')
        service_type = request.GET.get('type', None)

        if service_type is not None:
            if service_type in ALL_SERVICES:
                services = Service.objects.filter(service_type=service_type).values()
                return JsonResponse(list(services), safe=False)

        elif service_id is None:
            
            if state in ["PENDING", "ERROR", "REQUESTED", "COMPLETED"]:    
                services = Service.objects.filter(service_state=state).values()
            else:
                services = Service.objects.all().values()
            return JsonResponse(list(services), safe=False)

        else:
            s = Service.objects.filter(pk=service_id).values()[0]
            return JsonResponse(s, safe=False)

    #Pre: JSON with following format
    # { 
    #  "location": "LAB",
    #  "client": "client01",
    #  "service_type": "cpeless_irs",
    #  "id": "SVC001",
    #  "bandwidth": "10",
    #  "prefix":"29",
    #  "vrf_name" : '' // xPLS
    #  "client_network" : "192.168.0.0" // MPLS L3
    # }
    #
    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        client_name = data.pop('client')
        client = Client.objects.get(name=client_name)
        data['client_id'] = client.id

        location = data.pop('location')
        location_id = _get_location_id(location)

        free_access_port = _get_free_access_port(location_id)           
        access_port_id = str(free_access_port['id'])

        _use_port(access_port_id)
        data['access_port_id'] = access_port_id

        access_node_id = str(free_access_port['access_node_id'])
        data['vlan_id'] = _get_free_vlan_tag(access_node_id)['vlan_tag'] 
        data['access_node_id'] = access_node_id

        if data['service_type'] in VRF_SERVICES:

            if 'vrf_name' in data.keys():
                    vrf_name = data['vrf_name']
                    vrf = _get_vrf(vrf_name)
                    vrf_id = vrf['rt']
            else:
                vrf_list = _get_client_vrfs(client.name)

                vrf_name = "VPLS-" + client.name if data['service_type'] in VPLS_SERVICES else "VRF-" + client.name    
                vrf_name += "-" + str(len(vrf_list)+1) if vrf_list is not None else "-1"
                
                vrf = _get_free_vrf()
                if vrf is not None:
                    vrf_id = vrf['rt']
                    _use_vrf(vrf_id, vrf_name, client.name)
                else:
                    print("ERROR NON VRF AVAILABLE")
            
            data['vrf_id'] = vrf_id


        ServiceClass = getattr(models, ServiceTypes[data['service_type']].value)

        service = ServiceClass.objects.create(**data)
        service.service_state = "IN CONSTRUCTION"
        service.save()
        response = { "message": "Service requested" }

        return JsonResponse(response)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        print(data)

        service = Service.objects.filter(id=service_id)
        service.update(**data)

        return JsonResponse(data, safe=False)

class ServiceResourceView(View):

    def get(self, request, service_id=None):
        
        if service_id is not None:
            service = Service.objects.get(id=service_id)

            router_node = _get_router_node(service.router_node_id)
            access_node = _get_access_node(service.access_node_id)
            access_port = _get_access_port(service.access_port_id)
            client_node = _get_client_node(service.client_node_sn)

            data = { 'router_node': router_node,
                     'access_node': access_node,
                     'access_port': access_port['port'],
                     'client_node': client_node,
                     'logical_unit': service.logical_unit_id }
                
        
        return JsonResponse(data, safe=False)

def _get_router_node(router_node_id):
    url = settings.INVENTORY_URL + "routernodes/" + str(router_node_id)
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _get_access_node(access_node_id):
    url = settings.INVENTORY_URL + "accessnodes/" + str(access_node_id)
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _get_access_port(access_port_id):
    url = settings.INVENTORY_URL + "accessports/" + str(access_port_id)
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _get_client_node(client_node_id):
    url = settings.INVENTORY_URL + "clientnodes/" + str(client_node_id)
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _get_client_port(client_port_id):
    url = settings.INVENTORY_URL + "clientnodes/clientports" + str(client_node_id)
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


def _get_free_access_port(location_id):
    url = settings.INVENTORY_URL + "locations/"+ str(location_id) + "/accessports?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def _get_location_id(location_name):
    url= settings.INVENTORY_URL + "locations?name="+location_name
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]['id']
    else:
        return None

def _use_port(access_port_id):
    url= settings.INVENTORY_URL + "accessports/" + access_port_id
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _get_client_vrfs(client_name):
    url= settings.INVENTORY_URL + "vrfs?client="+client_name
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


def _get_free_vrf():
    url= settings.INVENTORY_URL + "vrfs?used=False"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None


def _use_vrf(vrf_id, vrf_name, client_name):
    url= settings.INVENTORY_URL + "vrfs/" + vrf_id
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True, "name": vrf_name, "client": client_name}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

#Returns first VLAN TAG free at access_node, if there is not free vlans available None value is returned.
def _get_free_vlan_tag(access_node_id):
    url = settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags?used=false"
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None


def _get_vrf(vrf_name):
    url = settings.INVENTORY_URL + "vrfs?name="+ vrf_name
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None