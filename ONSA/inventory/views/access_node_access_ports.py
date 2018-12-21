from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from inventory.models import AccessPort, AccessNode
from inventory.constants import *

import json

class AccessNodeAccessPortsView(View):
    def get(self, request, accessnode_id):
        
        used = request.GET.get('used', '').capitalize()
        if used == 'True':
            access_ports = AccessPort.objects.filter(access_node=accessnode_id,used=used).values()
        elif used == 'False':
            access_ports = AccessPort.objects.filter(access_node=accessnode_id,used=used).values()
        else:
            access_ports = AccessPort.objects.filter(access_node=accessnode_id).values()

        if list(access_ports) == []:
            return HttpResponse(status=ERR521)
        else:
            return JsonResponse(list(access_ports), safe=False)


    def post(self, request, accessnode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        access_node = AccessNode.objects.get(pk=accessnode_id)

        access_port = AccessPort.objects.create(**data, access_node=access_node)
        access_port.save()
        access_port = AccessPort.objects.filter(port=data['port']).values()
        
        return JsonResponse(list(access_port), safe=False)