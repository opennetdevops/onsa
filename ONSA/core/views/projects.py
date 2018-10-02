from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, Client
from enum import Enum
import json
import requests
from pprint import pprint


PROJECT_SERVICE_DEFINITION = "project"

class ProjectsView(View):

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        
        location = self._get_location(data['location_name'])


        """
        Fetch one access port in a given location.
        """
        free_access_port = _get_free_access_port(location['id'])
        access_port_id = str(free_access_port['id'])
        access_node_id = str(free_access_port['access_node_id'])

        """
        Fetch one vlan tag in a given access_node.
        """
        vlan_tag = _get_free_vlan_tag(access_node_id)



        #GET Client ID
        client = data.pop('client')
        client_obj = Client.objects.filter(name=client).values()[0]
        client_id = client_obj['id']
        data['client_id'] = client_id
        service_type = PROJECT_SERVICE_DEFINITION
        
        #request project at inventory
        _create_project(data['id'],access_node_id,access_port_id,vlan_tag)

        """
        Reserve previously fetched access port.
        """
        _use_port(access_port_id)

#TODO TBD
        client_obj = Client.objects.get(name=client)
        service = Service.objects.create(client=client_obj,id=data['id'],service_type=service_type)
        service.service_state = ServiceStates['REQUESTED'].value
        service.save()

        response = {"message" : "Project requested"}
        return JsonResponse(response)



    def put(self, request, product_id):

        data = json.loads(request.body.decode(encoding='UTF-8'))
        _update_product(product_id,data)
        return JsonResponse(data, safe=False)


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


def _update_product(product_id,data):
    url= settings.INVENTORY_URL + "products/" + product_id 
    rheaders = {'Content-Type': 'application/json'}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def _get_free_vlan_tag(self, access_node_id):
    url = settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags?used=false"
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None







