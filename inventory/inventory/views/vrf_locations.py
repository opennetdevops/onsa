# Django imports
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

# Python imports
import json

# ONSA imports
from inventory.models import Vrf, Location

class VrfLocationsView(View):
    def get(self, request, vrf_id, location_id=None):

        if location_id is not None:
            if Vrf.objects.filter(rt=vrf_id, locations=location_id).count() is not 0:
                exists = Vrf.objects.filter(rt=vrf_id, locations=location_id).values().count()
            else:
                JsonResponse({'message':"Not found"}, status=404)

            data = {}
            if exists:
                data["exists"] = True
            else:
                data["exists"] = False
            return JsonResponse(data, safe=False)

        else:
            try:
                vrf = Vrf.objects.get(rt=vrf_id)
            except ObjectDoesNotExist:
                return JsonResponse({'message':"Not found"}, status=404)
            return JsonResponse(list(vrf.locations.all().values()), safe=False)


    def put(self, request, vrf_id, location_id):
        location = Location.objects.get(pk=location_id)
        vrf = Vrf.objects.get(rt=vrf_id)
        vrf.locations.add(location)
        data = {"Message" : "Added location to vrf"}
        return JsonResponse(data, safe=False)


    def delete(self, request, vrf_id, location_id):
        vrf = Vrf.objects.filter(rt=vrf_id)
        location = Location.objects.get(pk=location_id)
        vrf.locations.remove(location)
        data = {"Message" : "Location deleted successfully from vrf"}
        return JsonResponse(data, safe=False)