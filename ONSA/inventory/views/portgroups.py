from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import Portgroup

import json

class PortgroupView(View):
    def get(self, request, portgroup_id=None):
        if not portgroup_id is None:
            portgroups = Portgroup.objects.filter(pk=portgroup_id).values()
            return JsonResponse(list(portgroups), safe=False)

        portgroups = Portgroup.objects.all().values()
        return JsonResponse(list(portgroups), safe=False)


    def put(self, request, portgroup_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        portgroup = Portgroup.objects.filter(pk=portgroup_id)
        portgroup.update(**data)
        my_portgroup = portgroup.values()
        return JsonResponse(list(my_portgroup), safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        portgroup = Portgroup.objects.create(**data)
        portgroup.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, portgroup_id):
        portgroup = Portgroup.objects.filter(pk=portgroup_id)
        portgroup.delete()
        data = {"Message" : "Virtual Pod deleted successfully"}
        return JsonResponse(data)