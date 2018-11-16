from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from enum import Enum
import json
import requests
from pprint import pprint

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']
PROJECT_SERVICES = ['projects']


def delete_charles_service(service_id):
    url = settings.CHARLES_URL + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def delete_jeangrey_service(service_id):
    url = settings.JEAN_GREY_URL + "services/"  + str(service_id)
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
        service = Service.objects.filter(id=service_id)
        service.update(**data)
        return JsonResponse(data, safe=False)

    def delete(self, request, service_id):
        delete_jeangrey_service(service_id)
        delete_charles_service(service_id)
        data = {"Message" : "Service deleted successfully"}
        return JsonResponse(data)

class ServiceResourcesView(View):
    def get(self, request, service_id=None):

        if service_id is not None:
            service = self.get_service(service_id)
            json_response = self.get_resources(service)

        return JsonResponse(json_response, safe=False)

    def _get_router_node(self, router_node_id):
        url = settings.INVENTORY_URL + "routernodes/" + router_node_id
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None

    def _get_access_node(self, access_node_id):
        url = settings.INVENTORY_URL + "accessnodes/" + str(access_node_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None

    def _get_access_port(self, access_port_id):
        url = settings.INVENTORY_URL + "accessports/" + str(access_port_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None

    def _get_client_node(self, client_node_id):
        url = settings.INVENTORY_URL + "clientnodes/" + str(client_node_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None

    def _get_client_port(self, client_node_sn, client_port_id):
        url = settings.INVENTORY_URL + "clientnodes/" + str(client_node_sn) + "/clientports/" + str(client_port_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None


    def _get_free_access_port(self, location_id):
        url = settings.INVENTORY_URL + "locations/"+ str(location_id) + "/accessports?used=false"
        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response[0]
        else:
            return None


    def _get_vrf(self, vrf_name):
        url = settings.INVENTORY_URL + "vrfs?name="+ vrf_name
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)
        if json_response:
            return json_response
        else:
            return None

    def get_service(self, service_id):
        url = settings.JEAN_GREY_URL + "services/" + str(service_id)
        rheaders = { 'Content-Type': 'application/json' }
        response = requests.get(url, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return json_response

    def get_resources(self, service):

        router_node = self._get_router_node(service['router_node_id'])
        access_node = self._get_access_node(service['access_node_id'])
        access_port = self._get_access_port(service['access_port_id'])

        resources = { "router_node": { 'name': router_node['name'] },
                      "access_node": { "model": access_node['model'],
                                       "name": access_node['name'],
                                       "access_port": access_port['port'] },
                      "vlan_id": service['vlan_id'],
                    }


        if service['service_state'] == 'REQUESTED':     
            client_node = self._get_client_node(service['client_node_sn'])

            resources['router_node']['logical_unit_id'] = service['logical_unit_id']

            if service['service_type'] == "vcpe_irs":
                resources['router_node']['vcpe_logical_unit_id'] = service['vcpe_logical_unit_id']

            resources["client_node"] = { "model": client_node['model'],
                                         "wan_port": client_node['uplink_port'] }

            if service['client_port_id'] is not None:
                client_port = self._get_client_port(service['client_node_sn'], service['client_port_id'])
                resources['client_node']['client_port'] = client_port['interface_name'] 
 
        
        return resources


