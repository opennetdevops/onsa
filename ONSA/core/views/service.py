from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, PublicIrsService, CpeLessIrsService, MplsService, ServiceFactory
from enum import Enum
from itertools import chain
import json

class ServiceStatuses(Enum):
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class ServiceView(View):

    def get(self, request):
        state = request.GET.get('state', '')

        if state in [ServiceStatuses['PENDING'].value, ServiceStatuses['ERROR'].value,
        ServiceStatuses['REQUESTED'].value, ServiceStatuses['COMPLETED'].value]:    
            pub_services = PublicIrsService.objects.filter(status=state).values()
            cpel_services = CpeLessIrsService.objects.filter(status=state).values()
            mpls_services = MplsService.objects.filter(status=state).values()

        else:
            pub_services = PublicIrsService.objects.all().values()
            cpel_services = CpeLessIrsService.objects.all().values()
            mpls_services = MplsService.objects.all().values()


        return JsonResponse(list(chain(pub_services, cpel_services, mpls_services)), safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = ServiceFactory.create(**data)
        service.service_state = ServiceStatuses['REQUESTED'].value
        service.save()
        response = {"message" : "Service requested"}
        return JsonResponse(response)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        service = Service.objects.filter(service_id=service_id)
        service.update(**data)
        return JsonResponse(data, safe=False)