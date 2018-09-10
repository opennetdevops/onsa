from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import Vrf, Location

import json

class VrfLocationsView(View):
    def get(self, request, vrf_id, location_id=None):

        if location_id is not None:
            exists = Vrf.objects.filter(rt=vrf_id, locations=location_id).values().count()
            if exists:
                return JsonResponse(True, safe=False)
            else:
                return JsonResponse(False, safe=False)

        else:
            vrf = Vrf.objects.get(rt=vrf_id)
            return JsonResponse(list(vrf.locations.all()), safe=False)


    def put(self, request, location_id):
        location = Location.objects.get(pk=location_id)
        vrf = Vrf.objects.get(rt=vrf_id)
        vrf.locations.add(location)
        return JsonResponse(vrf.values()[0], safe=False)


    def delete(self, request, vrf_id, location_id):
        vrf = Vrf.objects.filter(rt=vrf_id)
        location = Location.objects.get(pk=location_id)
        vrf.locations.remove(location)
        data = {"Message" : "Location deleted successfully from vrf"}
        return JsonResponse(data, safe=False)