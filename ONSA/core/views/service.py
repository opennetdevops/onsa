from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, ServiceCpeRelations
from enum import Enum
from itertools import chain
import json

class ServiceStates(Enum):
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class ServiceView(View):

    def get(self, request, service_id=None):
        state = request.GET.get('state', '')

        if service_id is None:
            if state in [ServiceStates['PENDING'].value, ServiceStates['ERROR'].value,
            ServiceStates['REQUESTED'].value, ServiceStates['COMPLETED'].value]:    
                services = ServiceCpeRelations.objects.filter(service__service_state=state).values()
            else:
                services = ServiceCpeRelations.objects.all().values()
            return JsonResponse(list(services), safe=False)

        else:
            s = Service.objects.get(service_id=service_id)
            return JsonResponse(s, safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.create(**data)
        service.service_state = ServiceStates['REQUESTED'].value
        service.save()
        response = {"message" : "Service requested"}
        return JsonResponse(response)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.objects.get(service_id)
        service.update(**data)
        return JsonResponse(data, safe=False)