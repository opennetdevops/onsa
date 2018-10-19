from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import ClientNodePort, ClientNode

import json

class ClientNodeClientPortsView(View):
    def get(self, request, client_node_sn, client_port_id=None):
        used = request.GET.get('used', '').capitalize()
        
        if client_port_id is None:
            if used:
                client_ports = ClientNodePort.objects.filter(client_node=client_node_sn, used=used).values()
                
            else:
                client_ports = ClientNodePort.objects.filter(client_node=client_node_sn).values()
 
            return JsonResponse(list(client_ports), safe=False)

        else:
            client_port = ClientNodePort.objects.filter(client_node=client_node_sn, pk=client_port_id).values()

            json_response = client_port[0] if len(client_port) else []

            return JsonResponse(json_response, safe=False)

    def put(self, request, client_node_sn, client_port_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_port = ClientNodePort.objects.filter(client_node=client_node_sn, pk=client_port_id)
        client_port.update(**data)
        
        my_client_node = client_port[0]
        my_client_node.save()
        return JsonResponse(list(client_port.values()), safe=False)


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