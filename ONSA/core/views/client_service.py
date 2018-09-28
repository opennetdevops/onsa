from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, Client
from enum import Enum
import json
import requests
from pprint import pprint

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']




class ClientServiceView(View):

    def get(self, request, client_id):
        service_type = request.GET.get('type', None)

        if service_type is not None:
            if service_type in ALL_SERVICES:
                services = Service.objects.filter(client=client_id, service_type=service_type).values()
        else:
            services = Service.objects.filter(client=client_id).values()

        return JsonResponse(list(services), safe=False)