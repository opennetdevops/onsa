from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, PublicIrsService, CpeLessIrsService, MplsService, ServiceFactory
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
                pub_services = PublicIrsService.objects.filter(service_state=state).values()
                cpel_services = CpeLessIrsService.objects.filter(service_state=state).values()
                mpls_services = MplsService.objects.filter(service_state=state).values()

            else:
                pub_services = PublicIrsService.objects.all().values()
                cpel_services = CpeLessIrsService.objects.all().values()
                mpls_services = MplsService.objects.all().values()

            return JsonResponse(list(chain(pub_services, cpel_services, mpls_services)), safe=False)
        else:
            s = ServiceFactory.get(service_id)
            return JsonResponse(list(s), safe=False)



    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = ServiceFactory.create(**data)
        service.service_state = ServiceStates['REQUESTED'].value
        service.save()
        response = {"message" : "Service requested"}
        return JsonResponse(response)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = ServiceFactory.get(service_id)
        service.update(**data)
        return JsonResponse(data, safe=False)