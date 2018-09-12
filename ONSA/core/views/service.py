from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, Client
from enum import Enum
import json
import requests
from pprint import pprint

# INVENTORY_URL = "http://127.0.0.1:8000/inventory/api/"
# CHARLES_URL = "http://127.0.0.1:8000/charles/api/services"
# BASE = "http://127.0.0.1:8000/"

class ServiceStates(Enum):
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    IN_CONSTRUCTION = "IN_CONSTRUCTION"
    ERROR = "ERROR"


class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')

        if service_id is None:
            if state in [ServiceStates['PENDING'].value, ServiceStates['ERROR'].value,
            ServiceStates['REQUESTED'].value, ServiceStates['COMPLETED'].value,
            ServiceStates['IN_CONSTRUCTION'].value]:    
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
    #  "client_id": 1,
    #  "service_type": "cpeless_irs",
    #  "id": "SVC001",
    #  "bandwidth": "10",
    #  "product_identifier":"PI0001",
    #  "prefix":"29",
    #  "vrf_name" : ''
    # }
    #
    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        pprint(data)

        #GET Client ID
        client = data.pop('client')
        client_obj = Client.objects.filter(name=client).values()[0]
        client_id = client_obj['id']
        data['client_id'] = client_id
        
        #GET Location ID
        print(data['location'])
        location_id = _get_location_id(data['location'])
        print(location_id)

        #GET access_port from inventory
        free_access_port = _get_free_access_port(location_id)
        access_port_id = str(free_access_port['id'])
        print(access_port_id)


        #PUT to inventory to set access_port used
        _use_port(access_port_id)


        #Create VRF
        if data['vrf_name'] is '':
            #Get client VRFs
            vrfs = _get_client_vrfs(client_obj['name'])
            #Create VRF
            vrf_name = "VRF-" + client_obj['name'] + str(len(vrfs)+1)
            _create_vrf(vrf_name)
            #TODO VRF based on service type
            
        else:
            service.vrf_name = data['vrf_name']

        data['access_node_port'] = access_port_id
        data['access_node'] = str(free_access_port['accessNode_id'])
        service = Service.objects.create(**data)
        service.service_state = ServiceStates['IN_CONSTRUCTION'].value
        service.save()
        response = {"message" : "Service requested"}
        return JsonResponse(response)

    def put(self, request, service_id):
        #To change state and client_network/wan_ip
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.objects.filter(id=service_id)
        service.update(**data)
        return JsonResponse(data, safe=False)

def _get_free_access_port(location_id):
    url= settings.INVENTORY_URL + "locations/"+ str(location_id) + "/accessports?used=false"
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







