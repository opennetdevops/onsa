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

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')
        service_type = request.GET.get('type', None)
        vrf_id = request.GET.get('vrf_id',None)

        if vrf_id is not None:

            cpeless_mpls_services = list(CpelessMpls.objects.filter(vrf_id=vrf_id).values())
            cpe_mpls_services = list(CpeMpls.objects.filter(vrf_id=vrf_id).values())
            vpls_services = list(Vpls.objects.filter(vrf_id=vrf_id).values())

            services = cpe_mpls_services + cpeless_mpls_services + vpls_services
            return JsonResponse(services, safe=False)


        if service_type is not None:
            if service_type in ALL_SERVICES:
                ServiceClass = getattr(models, ServiceTypes[service_type].value)
                services = ServiceClass.objects.filter(service_type=service_type).values()
                return JsonResponse(list(services), safe=False)

        elif service_id is None:            
            if state in ["PENDING", "ERROR", "REQUESTED", "COMPLETED"]:
                cpeless_irs_services = list(CpelessIrs.objects.filter(service_state=state).values())
                cpe_irs_services = list(CpeIrs.objects.filter(service_state=state).values())
                cpeless_mpls_services = list(CpelessMpls.objects.filter(service_state=state).values())
                cpe_mpls_services = list(CpeMpls.objects.filter(service_state=state).values())
                vcpe_irs_services = list(VcpeIrs.objects.filter(service_state=state).values())    
                vpls_services = list(Vpls.objects.filter(service_state=state).values())

                services = cpe_mpls_services + cpeless_irs_services + cpeless_mpls_services \
                 + vpls_services + vcpe_irs_services + cpe_irs_services

            else:
                cpeless_irs_services = list(CpelessIrs.objects.all().values())
                cpe_irs_services = list(CpeIrs.objects.all().values())
                cpeless_mpls_services = list(CpelessMpls.objects.all().values())
                cpe_mpls_services = list(CpeMpls.objects.all().values())
                vcpe_irs_services = list(VcpeIrs.objects.all().values()) 
                vpls_services = list(Vpls.objects.all().values())

                pprint(vcpe_irs_services)

                services = cpe_mpls_services + cpeless_irs_services + cpeless_mpls_services \
                 + vpls_services + vcpe_irs_services + cpe_irs_services

            return JsonResponse(services, safe=False)

        else:
            s = Service.objects.filter(pk=service_id).values()[0]
            ServiceClass = getattr(models, ServiceTypes[s['service_type']].value)
            s = ServiceClass.objects.filter(pk=service_id).values()[0]
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
 
        data = self.define_vrf(client, data)

        data['location_id'] = location_id
        data['router_node_id'] = router_node['id']
        data['access_port_id'] = access_port_id
        data['client_id'] = client.id
        data['vlan_id'] = vlan['vlan_tag']
        data['access_node_id'] = access_node_id

        ServiceClass = getattr(models, ServiceTypes[data['service_type']].value)

        service = ServiceClass.objects.create(**data)
        service.service_state = "IN CONSTRUCTION"
        service.save()
        response = { "message": "Service requested" }

        return JsonResponse(response)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        service_type = Service.objects.get(id=service_id).service_type
        ServiceClass = getattr(models, ServiceTypes[service_type].value)
        
        service = ServiceClass.objects.filter(id=service_id)
        service.update(**data)

        return JsonResponse(data, safe=False)

    def define_vrf(self, client, data):
        if data['service_type'] in VRF_SERVICES:

            if 'vrf_name' in data.keys():
                    vrf_name = data.pop('vrf_name')
                    vrf = get_vrf(vrf_name)
                    vrf_id = vrf['rt']
            else:
                vrf_list = get_client_vrfs(client.name)

                vrf_name = "VPLS-" + client.name if data['service_type'] in VPLS_SERVICES else "VRF-" + client.name    
                vrf_name += "-" + str(len(vrf_list)+1) if vrf_list is not None else "-1"
                
                vrf = get_free_vrf()
                if vrf is not None:
                    vrf_id = vrf['rt']
                    use_vrf(vrf_id, vrf_name, client.name)
                else:
                    print("ERROR NON VRF AVAILABLE")
            
            data['vrf_id'] = vrf_id
            data['autonomous_system'] = assign_autonomous_system(vrf_id)

        return data