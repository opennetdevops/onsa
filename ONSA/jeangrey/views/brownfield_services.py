from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from jeangrey.models import Client, Service, CpelessIrs, CpeMpls, CpeIrs, Vpls, VcpeIrs, CpelessMpls
from jeangrey import models
from jeangrey.utils.utils import *
from enum import Enum
import json
import requests

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

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        client_name = data.pop('client')
        client = Client.objects.get(name=client_name)
        
        location = data.pop('location')
        location_id = get_location_id(location)
        router_node = get_router_node(location_id)
      
        if 'client_node_sn' in data.keys():
            access_port_id = Service.objects.filter(client_node_sn=data['client_node_sn']).values()[0]['access_port_id']
            access_port = get_access_port(access_port_id)
            access_node_id = access_port['access_node_id']

        else:
            free_access_port = get_free_access_port(location_id)           
            access_port_id = str(free_access_port['id'])
            use_port(access_port_id)
            access_node_id = str(free_access_port['access_node_id'])

        vlan = get_free_vlan(access_node_id)
        use_vlan(access_node_id, vlan['vlan_tag'])
 
        data['location_id'] = location_id
        data['router_node_id'] = router_node['id']
        data['access_port_id'] = access_port_id
        data['client_id'] = client.id
        data['vlan_id'] = vlan['vlan_tag']
        data['access_node_id'] = access_node_id

        ServiceClass = getattr(models, ServiceTypes[data['service_type']].value)

        service = ServiceClass.objects.create(**data)
        service.service_state = "BF_IN_CONSTRUCTION"
        service.save()
        response = { "message": "Service requested" }

        return JsonResponse(response)