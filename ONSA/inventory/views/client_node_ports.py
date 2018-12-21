# Django imports
from django.core import serializers
from django.http import JsonResponse
from django.views import View

# Python imports
import json

# ONSA imports
from inventory.models import ClientNodePort



class ClientNodePortsView(View):
    def get(self, request, client_port_id=None):
        if client_port_id is not None:
            client_port = ClientNodePort.objects.filter(pk=client_port_id).values()[0]
            return JsonResponse(client_port, safe=False)
        else:
            client_ports = ClientNodePort.objects.all().values()
            return JsonResponse(list(client_ports), safe=False)

    def put(self, request, client_port_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_port = ClientNodePort.objects.filter(pk=client_port_id)
        client_port.update(**data)
        my_client_node = client_port.values()[0]
        return JsonResponse(my_client_node, safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_port = ClientNodePort.objects.create(**data)
        client_port.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, client_node_sn, client_port_id):
        client_port = ClientNodePort.objects.filter(client_node=client_node_sn)
        client_port.delete()
        data = {"Message" : "Client Node Port deleted successfully"}
        return JsonResponse(data)