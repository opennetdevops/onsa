from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import ClientNode

import json

class ClientNodesView(View):
    def get(self, request, client_node_sn=None):

        if not client_node_sn is None:
            client_node = ClientNode.objects.filter(serial_number=client_node_sn).values()[0]
            return JsonResponse(client_node, safe=False)

        else:
            client_nodes = ClientNode.objects.all().values()
            return JsonResponse(list(client_nodes), safe=False)



    def put(self, request, client_node_sn):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_node = ClientNode.objects.filter(serial_number=client_node_sn)
        client_node.update(**data)
        my_client_node = client_node.values()[0]
        return JsonResponse(my_client_node, safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_node = ClientNode.objects.create(**data)
        client_node.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, client_node_sn):
        client_node = ClientNode.objects.filter(serial_number=client_node_sn)
        client_node.delete()
        data = {"Message" : "Client Node deleted successfully"}
        return JsonResponse(data)