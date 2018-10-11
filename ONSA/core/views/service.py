from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, Client
from enum import Enum
import json
import requests
from pprint import pprint

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']
PROJECT_SERVICES = ['projects']

class ServiceStates(Enum):
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    IN_CONSTRUCTION = "IN_CONSTRUCTION"
    ERROR = "ERROR"


class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')
        service_type = request.GET.get('type', None)

        if service_type is not None:
            if service_type in ALL_SERVICES:
                services = Service.objects.filter(service_type=service_type).values()
                return JsonResponse(list(services), safe=False)

        elif service_id is None:
            
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

        #GET Client ID
        client = data.pop('client')
        client_obj = Client.objects.filter(name=client).values()[0]
        client_id = client_obj['id']
        product_id = data['id']
        bandwidth = data.pop('bandwidth')

        data['client_id'] = client_id
        service_type = data['service_type']
        location = data.pop('location')

        

        try:
            location_id = _get_location_id(location)
            print("loc id: ",location_id)
            #GET access_port from inventory
            free_access_port = _get_free_access_port(location_id)
            print("free acc port: ",free_access_port)
            access_port_id = str(free_access_port['id'])
            print("access port id: ",access_port_id)
            #PUT to inventory to set access_port used
            _use_port(access_port_id)

            #data['access_node_port'] = access_port_id
            access_node_id = str(free_access_port['access_node_id'])
            vlan_tag = _get_free_vlan_tag(access_node_id)
            print("vlan tag: ",vlan_tag)

        #TODO ASCO
        except KeyError:
            print("exception error")
            pass

        #Create VRF
        #todo rewrite splitting service type
        if 'vrf_name' in data.keys():
            if data['vrf_name'] is '' and (data['service_type'] in VRF_SERVICES):
                
                data.pop('vrf_name')

                #Get client VRFs
                vrfs = _get_client_vrfs(client_obj['name'])

                if data['service_type'] in VPLS_SERVICES:
                    vrf_name = "VPLS-"
                else:
                    vrf_name = "VRF-"

                #Create VRF Name
                if vrfs is not None:
                    vrf_name = vrf_name + client_obj['name'] + "-" + str(len(vrfs)+1)
                else:
                    vrf_name = vrf_name + client_obj['name'] + "-1"
                
                vrf = _get_free_vrf()
                
                if vrf is not None:
                    _use_vrf(vrf['rt'],vrf_name, client_obj['name'])
                    vrf_id = vrf['rt']
                    data['vrf_name'] = vrf_name
                else:
                    print("ERROR NON VRF AVAILABLE")
                #todo release port
                #TODO HANDLE ERROR
            else:
                vrf_name = data['vrf_name']
                vrf = _get_vrf(vrf_name)
                vrf_id = vrf['rt']



        #Create at inventory model
        _create_product(product_id,access_node_id,access_port_id,vlan_tag['vlan_tag'], bandwidth, vrf_id)


        #Save at core model
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

def _create_product(product_id,access_node_id,access_port_id,vlan_tag, bandwidth, vrf_id):
    url= settings.INVENTORY_URL + "products/" + product_id 
    rheaders = {'Content-Type': 'application/json'}
    data = {
            "access_node_id":access_node_id,
            "access_port_id":access_port_id,
            "vlan_tag":vlan_tag,
            "bandwidth":bandwidth,
            "vrf_id":vrf_id
            }
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
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




