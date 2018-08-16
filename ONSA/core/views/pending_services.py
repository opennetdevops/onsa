from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Service, ServiceCpeRelations
from enum import Enum
from itertools import chain
import json



class PendingServiceView(View):

    def get(self, request):
        state = request.GET.get('state', '')

        if not state:
            s = ServiceCpeRelations.objects.all().values()
        else:
            s = ServiceCpeRelations.objects.filter(service_state=state).values()

        return JsonResponse(list(s), safe=False)




