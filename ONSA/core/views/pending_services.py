from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, ServiceCpeRelations
from enum import Enum
from itertools import chain
import json



class PendingServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')

        if service_id is None:
            if not state:
                s = ServiceCpeRelations.objects.all().values()
            else:
                s = ServiceCpeRelations.objects.filter(service_state=state).values()

            return JsonResponse(list(s), safe=False)
        else:
            s = ServiceCpeRelations.objects.filter(service__pk=service_id).values()[0]
            return JsonResponse(s, safe=False)

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




