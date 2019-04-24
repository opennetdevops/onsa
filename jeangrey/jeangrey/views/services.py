from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from jeangrey.models import *
from jeangrey.utils import *
from jeangrey.forms import ServiceForm

import jeangrey.models as models

from rest_framework.views import APIView

#serializer trial:
from ..utils.swagger_util import ServiceSerializer
from drf_yasg.utils import no_body, swagger_auto_schema



import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)



class ServiceView(View):
# changed base class from View to APIVew.
    @swagger_auto_schema(
    # query_serializer=ListQuerySerializer, # query params serializar
    responses={200: ServiceSerializer(many=True)}, # response serializer
    operation_description="Obtain the actual status of the device.", tags=['services'],
    
     )
    def get(self, request, service_id=None):
        state = request.GET.get('state', '')
        service_type = request.GET.get('type', None)
        vrf_id = request.GET.get('vrf_id', None)

        try:
            if vrf_id is not None:
                cpeless_mpls_services = list(
                    CpelessMpls.objects.filter(vrf_id=vrf_id).values())
                cpe_mpls_services = list(
                    CpeMpls.objects.filter(vrf_id=vrf_id).values())
                vpls_services = list(
                    Vpls.objects.filter(vrf_id=vrf_id).values())

                services = cpe_mpls_services + cpeless_mpls_services + vpls_services
                return JsonResponse(services, safe=False)

            if service_type is not None:
                ServiceClass = getattr(models, ServiceTypes[service_type])
                services = ServiceClass.objects.filter(
                    service_type=service_type).values()
                return JsonResponse(list(services), safe=False)

            elif service_id is None:
                if state in ["PENDING", "ERROR", "REQUESTED", "COMPLETED"]:
                    cpeless_irs_services = list(
                        CpelessIrs.objects.filter(service_state=state).values())
                    cpe_irs_services = list(
                        CpeIrs.objects.filter(service_state=state).values())
                    cpeless_mpls_services = list(
                        CpelessMpls.objects.filter(service_state=state).values())
                    cpe_mpls_services = list(
                        CpeMpls.objects.filter(service_state=state).values())
                    vcpe_irs_services = list(
                        VcpeIrs.objects.filter(service_state=state).values())
                    vpls_services = list(Vpls.objects.filter(
                        service_state=state).values())

                    services = cpe_mpls_services + cpeless_irs_services + cpeless_mpls_services \
                        + vpls_services + vcpe_irs_services + cpe_irs_services

                else:
                    cpeless_irs_services = list(
                        CpelessIrs.objects.all().values())
                    cpe_irs_services = list(CpeIrs.objects.all().values())
                    cpeless_mpls_services = list(
                        CpelessMpls.objects.all().values())
                    cpe_mpls_services = list(CpeMpls.objects.all().values())
                    vcpe_irs_services = list(VcpeIrs.objects.all().values())
                    vpls_services = list(Vpls.objects.all().values())

                    services = cpe_mpls_services + cpeless_irs_services + cpeless_mpls_services \
                        + vpls_services + vcpe_irs_services + cpe_irs_services

                return JsonResponse(services, safe=False)

            else:
                s = Service.objects.get(pk=service_id)
                ServiceClass = getattr(models, ServiceTypes[s.service_type])
                s = ServiceClass.objects.get(pk=service_id)
                data = s.fields()

                return JsonResponse(data, safe=False)

        except Service.DoesNotExist as e:
            logging.error(e)
            return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)
        except KeyError:
            return JsonResponse([], safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        form = ServiceForm(data)

        if form.is_valid():

            try:
                client_name = data.pop('client')
                client = Client.objects.get(name=client_name)

                location = data.pop('location')
                location_id = get_location_id(location)
                router_node = get_router_node(location_id)

                if "access_port_id" not in data.keys():
                    access_port = get_free_access_port(location_id)
                    access_port_id = str(access_port['id'])
                    use_access_port(access_port_id)
                else:
                    access_port_id = data['access_port_id']
                    access_port = get_access_port(access_port_id)

                access_node_id = str(access_port['access_node_id'])

                vlan = get_free_vlan(access_node_id)

                # todo pasar exception

                use_vlan(access_node_id, vlan['id'])

                data['location_id'] = location_id
                data['router_node_id'] = router_node['id']
                data['access_port_id'] = access_port_id
                data['client_id'] = client.id
                data['vlan_id'] = vlan['vlan_tag']
                data['access_node_id'] = access_node_id
                data['customer_location_id'] = int(
                    data['customer_location_id'])

                ServiceClass = getattr(
                    models, ServiceTypes[data['service_type']])

                service = ServiceClass.objects.create(**data)
                service.service_state = INITIAL_SERVICE_STATE
                service.save()

                return JsonResponse(service.fields(), safe=False, status=HTTP_201_CREATED)

            except CustomException as e:
                return e.handle()
            except Client.DoesNotExist as e:
                logging.error(e)
                return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)

        else:
            json_response = {"msg": "Form is invalid.", "errors": form.errors}
            return JsonResponse(json_response, safe=False, status=ERR_BAD_REQUEST)

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
            return HttpResponse(status=HTTP_204_NO_CONTENT)

        except Service.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
