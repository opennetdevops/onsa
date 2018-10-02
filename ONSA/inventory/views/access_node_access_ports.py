from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import AccessPort, AccessNode

import json

class AccessNodeAccessPortsView(View):
    def get(self, request, accessnode_id):
        
        used = request.GET.get('used', '')
        if used == "true":
            access_ports = AccessPort.objects.filter(access_node=accessnode_id,used=True).values()
        elif used == "false":
            access_ports = AccessPort.objects.filter(access_node=accessnode_id,used=False).values()
        else:
            access_ports = AccessPort.objects.filter(access_node=accessnode_id).values()

        return JsonResponse(list(access_ports), safe=False)


    def post(self, request, accessnode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        access_node = AccessNode.objects.get(pk=accessnode_id)

        access_port = AccessPort.objects.create(**data, access_node=access_node)
        access_port.save()
        access_port = AccessPort.objects.filter(port=data['port']).values()
        
        return JsonResponse(list(access_port), safe=False)