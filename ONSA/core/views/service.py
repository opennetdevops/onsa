from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service
from enum import Enum
from itertools import chain
import json

class ServiceStates(Enum):
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    IN_CONSTRUCTION = "IN_CONSTRUCTION"
    ERROR = "ERROR"


class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')

        if service_id is None:
            if state in [ServiceStates['PENDING'].value, ServiceStates['ERROR'].value,
            ServiceStates['REQUESTED'].value, ServiceStates['COMPLETED'].value,
            ServiceStates['IN_CONSTRUCTION']].value:    
                services = Service.objects.filter(service_state=state).values()
            else:
                services = Service.objects.all().values()
            return JsonResponse(list(services), safe=False)

        else:
            s = Service.objects.filter(pk=service_id).values()[0]
            return JsonResponse(s, safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        
        #GET access_port from inventory
        
        #PUT to inventory to set access_port used 


        service = Service.create(**data)
        service.service_state = ServiceStates['IN_CONSTRUCTION'].value
        service.save()
        response = {"message" : "Service requested"}
        return JsonResponse(response)

    def put(self, request, service_id):
        #To change state only
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.objects.get(service_id)
        service.update(**data)
        return JsonResponse(data, safe=False)