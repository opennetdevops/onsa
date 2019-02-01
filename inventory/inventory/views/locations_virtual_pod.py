from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import Location, VirtualVmwPod
from inventory.constants import *
from inventory.exceptions import *

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class LocationVirtualPodView(View):
    def get(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id)
            all_virtual_pods = VirtualVmwPod.objects.filter(location=location).values()
            return JsonResponse(list(all_virtual_pods), safe=False)
        except Location.DoesNotExist:
            return JsonResponse({'message':"Not found"}, status=ERR_NOT_FOUND)
