from django.core import serializers
from django.http import JsonResponse
from django.views import View
from ..models import Location, AccessNode, AccessPort

import json

class LocationAccessPortsView(View):
    def get(self, request, location_id):

        access_nodes =  AccessNode.objects.filter(location_id=location_id)
        all_ports = []
        used = request.GET.get('used', '')

        for an in access_nodes:
            if used == "true":
                my_ports = AccessPort.objects.filter(access_node=an, used=True).values()
                for port in my_ports:
                    all_ports.append(port)
            elif used == "false":
                my_ports = AccessPort.objects.filter(access_node=an, used=False).values()
                for port in my_ports:
                    all_ports.append(port)
            else:
                my_ports = AccessPort.objects.filter(access_node=an).values()
                for port in my_ports:
                    all_ports.append(port)

        return JsonResponse(list(all_ports), safe=False)
