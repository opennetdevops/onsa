from django.core import serializers
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from ..models import Location, VirtualVmwPod

import json

class LocationVirtualPodView(View):
    def get(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id)
            all_virtual_pods = VirtualVmwPod.objects.filter(location=location).values()
            return JsonResponse(list(all_virtual_pods), safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'message':"Not found"}, status=404)
