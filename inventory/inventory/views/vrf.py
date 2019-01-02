from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import Vrf, Location

import json

class VrfView(View):
    def get(self, request, vrf_id=None):
        if vrf_id is not None:
            vrf = Vrf.objects.filter(rt=vrf_id).values()[0]
            return JsonResponse(vrf, safe=False)
        name = request.GET.get('name')
        client = request.GET.get('client')
        used = request.GET.get('used')
       
        if name is not None:
            if Vrf.objects.filter(name=name).count() is not 0:
                vrf = Vrf.objects.filter(name=name).values()[0]
                return JsonResponse(vrf, safe=False)
            else:
                return JsonResponse({}, safe=False)
       
        elif client is not None:
            if Vrf.objects.filter(client=client).count() is not 0:
                vrf = Vrf.objects.filter(client=client).values()
                return JsonResponse(list(vrf), safe=False)
            else:
                return JsonResponse({}, safe=False)

        elif used is not None:
            vrfs = Vrf.objects.filter(used=used).values()
            return JsonResponse(list(vrfs), safe=False)

        else:
            vrfs = Vrf.objects.all().values()
            return JsonResponse(list(vrfs), safe=False)


    def put(self, request, vrf_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        vrf = Vrf.objects.filter(rt=vrf_id)
        vrf.update(**data)
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