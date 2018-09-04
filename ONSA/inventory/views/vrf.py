from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import Vrf, Location, Services

import json

class VrfView(View):
    def get(self, request, vrf_id=None):

        if vrf_id is not None:
            vrf = Vrf.objects.filter(rt=vrf_id).values()[0]
            return JsonResponse(vrf, safe=False)

        service_id = request.GET.get('service_id')

        if service_id is not None:
            vrfs = Vrf.objects.filter(service_id=service_id)
        else:
            vrfs = Vrf.objects.all().values()
            
        return JsonResponse(list(vrfs), safe=False)

    def put(self, request, vrf_id=None):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        location = Location.objects.get(name=data['location_name'])
        vrf = Vrf.objects.get(rt=vrf_id)
        vrf.add(locations=location)
        return JsonResponse(vrf.values()[0], safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        location = Location.objects.filter(name=data['location_name'])
        vrf = Vrf.objects.create(**data)
        vrf.save()
        return JsonResponse(vrf.values()[0], safe=False)       


    def delete(self, request, vrf_id):
        vrf = Vrf.objects.filter(rt=vrf_id)
        vrf.delete()
        data = {"Message" : "Virtual Pod deleted successfully"}
        return JsonResponse(data, safe=False)