from django.conf import settings
from django.http import JsonResponse
from django.views import View
from jeangrey.models import *
from jeangrey.utils import *
import jeangrey.models as models

import json
import requests
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')
        service_type = request.GET.get('type', None)
        vrf_id = request.GET.get('vrf_id',None)

        try:
            if vrf_id is not None:
                cpeless_mpls_services = list(CpelessMpls.objects.filter(vrf_id=vrf_id).values())
                cpe_mpls_services = list(CpeMpls.objects.filter(vrf_id=vrf_id).values())
                vpls_services = list(Vpls.objects.filter(vrf_id=vrf_id).values())

                services = cpe_mpls_services + cpeless_mpls_services + vpls_services
                return JsonResponse(services, safe=False)

            if service_type is not None:
                ServiceClass = getattr(models, ServiceTypes[service_type])
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

                    services = cpe_mpls_services + cpeless_irs_services + cpeless_mpls_services \
                    + vpls_services + vcpe_irs_services + cpe_irs_services

                return JsonResponse(services, safe=False)

            else:
                s = Service.objects.filter(pk=service_id).values()[0]
                ServiceClass = getattr(models, ServiceTypes[s['service_type']])
                s = ServiceClass.objects.filter(pk=service_id).values()[0]
                return JsonResponse(s, safe=False)

        except IndexError:
            msg = "Service not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except KeyError:
            msg = "Service type does not exist."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
            

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        try:        
            client_name = data.pop('client')
            client = Client.objects.get(name=client_name)

            location = data.pop('location')
            location_id = get_location_id(location)
            router_node = get_router_node(location_id)

            if "access_port_id" not in data.keys():
                access_port = get_free_access_port(location_id)           
                access_port_id = str(access_port['id'])
                use_port(access_port_id)
            else:
                access_port_id = data['access_port_id']
                access_port = get_access_port(access_port_id)

            access_node_id = str(access_port['access_node_id'])

            vlan = get_free_vlan(access_node_id)
            #todo pasar exception
            use_vlan(access_node_id, vlan['vlan_tag'])
    
            data['location_id'] = location_id
            data['router_node_id'] = router_node['id']
            data['access_port_id'] = access_port_id
            data['client_id'] = client.id
            data['vlan_id'] = vlan['vlan_tag']
            data['access_node_id'] = access_node_id
            data['customer_location_id'] = int(data['customer_location_id'])

            ServiceClass = getattr(models, ServiceTypes[data['service_type']])

            service = ServiceClass.objects.create(**data)
            service.service_state = "in_construction"
            service.save()

            return JsonResponse({ "msg": "Service requested" }, safe=False)
        
        except LocationException as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except RouterNodeException as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except AccessPortException as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except VlanException as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NO_VLANS)
        except Client.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except KeyError:
            logging.error("Bad Request")
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_BAD_REQUEST)
        
    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        try:
            service_type = Service.objects.get(id=service_id).service_type
            ServiceClass = getattr(models, ServiceTypes[service_type])
            
            service = ServiceClass.objects.filter(id=service_id)
            service.update(**data)

            return JsonResponse(ServiceClass.objects.filter(id=service_id).values()[0], safe=False)
        except Service.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def delete(self, request, service_id):
        try:
            svc = Service.objects.get(id=service_id)
            svc.delete()
            data = {"Message" : "Service deleted successfully"}
            return JsonResponse(data)
        except Service.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    