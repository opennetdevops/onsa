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


class ProjectsView(View):

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

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        #GET Client ID
        client = data.pop('client')
        client_obj = Client.objects.filter(name=client).values()[0]
        client_id = client_obj['id']
        data['client_id'] = client_id
        service_type = data['service_type']
        
        if service_type in PROJECT_SERVICES:
            #request project at inventory
            _create_project(data['id'],data['access_node_id'],data['access_port_id'],data['vlan_tag'])
            client_obj = Client.objects.get(name=client)
            service = Service.objects.create(client=client_obj,id=data['id'],service_type=service_type)
            service.service_state = ServiceStates['REQUESTED'].value
            service.save()


            response = {"message" : "Project requested"}
            return JsonResponse(response)

        else: 
            #GET Location ID
            try:
                location_id = _get_location_id(data['location'])

                #GET access_port from inventory
                free_access_port = _get_free_access_port(location_id)
                access_port_id = str(free_access_port['id'])
                #PUT to inventory to set access_port used
                _use_port(access_port_id)

                data['access_node_port'] = access_port_id
                data['access_node'] = str(free_access_port['accessNode_id'])

            #TODO ASCO
            except KeyError:
                pass

            #Create VRF
            #todo rewrite splitting service type
            if 'vrf_name' in data.keys():
                if data['vrf_name'] is '' and (data['service_type'] in VRF_SERVICES):
                    
                    #Get client VRFs
                    vrfs = _get_client_vrfs(client_obj['name'])
                    if data['service_type'] in VPLS_SERVICES:
                        vrf_name = "VPLS-"
                    else:
                        vrf_name = "VRF-"

                    #Create VRF
                    if vrfs is not None:
                        vrf_name = vrf_name + client_obj['name'] + "-" + str(len(vrfs)+1)
                    else:
                        vrf_name = vrf_name + client_obj['name'] + "-1"
                    
                    vrf = _get_free_vrf()
                    
                    if vrf is not None:
                        _use_vrf(vrf['rt'],vrf_name, client_obj['name'])
                        data['vrf_name'] = vrf_name
                    else:
                        print("ERROR NON VRF AVAILABLE")
                    #todo release port
                    #TODO HANDLE ERROR
                #TODO VRF based on service type

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

def _create_project(product_id,access_node_id,access_port_id,vlan_tag):
    url= settings.INVENTORY_URL + "products/" + product_id 
    rheaders = {'Content-Type': 'application/json'}
    data = {
            "access_node_id":access_node_id,
            "access_port_id":access_port_id,
            "vlan_tag":vlan_tag
            }
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None







