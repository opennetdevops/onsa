from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from inventory.models import AccessPort

import json

class AccessPortsView(View):
    def get(self, request, accessport_id=None):
        if accessport_id is None:
            access_ports = AccessPort.objects.all().values()
            return JsonResponse(list(access_ports), safe=False)
        else:
            try:
                access_port = AccessPort.objects.filter(pk=accessport_id).values()[0]   
                return JsonResponse(access_port, safe=False)
            except IndexError:
                return HttpResponse(status=500)


    def put(self, request, accessport_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        access_port = AccessPort.objects.filter(pk=accessport_id)
        access_port.update(**data)
        my_access_port = access_port.values()
        
        return JsonResponse(list(my_access_port), safe=False)


    def delete(self, request, accessport_id):
        access_port = AccessPort.objects.filter(pk=accessport_id)
        access_port.delete()
        
        data = {"Message" : "AccessPort deleted successfully"}
        return JsonResponse(data)