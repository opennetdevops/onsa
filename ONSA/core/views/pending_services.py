from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, ServiceCpeRelations
from enum import Enum
from itertools import chain
import json

from pprint import pprint



class PendingServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')

        if service_id is None:
            services_info = []

            s = ServiceCpeRelations.objects.all() if not state else ServiceCpeRelations.objects.filter(service__service_state=state)

            for relation in s:
                info = { 'client_name' : relation.service.client.name,
                                     'client_node_sn' : relation.cpe_port.cpe.serial_number,
                                     'client_node_port' : relation.cpe_port.name,
                                     'bandwidth' : relation.service.bandwidth,
                                     'prefix' : relation.service.prefix,
                                     'vrf' : relation.service.vrf,
                                     'service_state' : relation.service.service_state,
                                     'product_identifier' : relation.service.product_identifier,
                                     'service_type' : relation.service.service_type,
                                     'service_id' : relation.service.id }

                services_info.append(info)

            return JsonResponse(services_info, safe=False)

        else:
            s = ServiceCpeRelations.objects.get(service__pk=service_id)

            service_info = { 'client_name' : s.service.client.name,
                             'client_node_sn' : s.cpe_port.cpe.serial_number,
                             'client_node_port' : s.cpe_port.name,
                             'bandwidth' : s.service.bandwidth,
                             'prefix' : s.service.prefix,
                             'vrf' : s.service.vrf,
                             'service_state' : s.service.service_state,
                             'product_identifier' : s.service.product_identifier,
                             'service_type' : s.service.service_type }

            return JsonResponse(service_info, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        
        #data['sn']
        #GET CPE from inventory


        service = ServiceCpeRelations.create(**data)
        service.service_state = ServiceStates['REQUESTED'].value
        service.save()
        response = {"message" : "Service requested"}
        return JsonResponse(response)


    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.objects.filter(pk=service_id)
        service_relation = ServiceCpeRelations.objects.filter(service__pk=service_id)
        service_relation.update(**data)
        service.update(**data)

        return JsonResponse(data, safe=False)




