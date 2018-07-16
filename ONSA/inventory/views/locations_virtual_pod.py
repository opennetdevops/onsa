from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import Location, VirtualVmwPod

import json

class LocationVirtualPodView(View):
    def get(self, request, location_id):
        location = Location.objects.get(pk=location_id)
        all_virtual_pods = VirtualVmwPod.objects.filter(location=location).values()
        return JsonResponse(list(all_virtual_pods), safe=False)
