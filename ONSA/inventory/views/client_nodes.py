from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import ClientNode

import json

class ClientNodesView(View):
    def get(self, request, client_node_id=None):
        sn = request.GET.get('sn')

        if not client_node_id is None:
            client_node = ClientNode.objects.filter(pk=client_node_id).values()[0]
            return JsonResponse(client_node, safe=False)

        elif not sn:
            client_nodes = ClientNode.objects.all().values()
            return JsonResponse(list(client_nodes), safe=False)

        else:
            client_node = ClientNode.objects.filter(serial_number=sn).values()[0]
            return JsonResponse(client_node, safe=False)


    def put(self, request, client_node_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_node = ClientNode.objects.filter(pk=client_node_id)
        client_node.update(**data)
        my_client_node = client_node.values()[0]
        return JsonResponse(my_client_node, safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_node = ClientNode.objects.create(**data)
        client_node.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, client_node_id):
        client_node = ClientNode.objects.filter(pk=client_node_id)
        client_node.delete()
        data = {"Message" : "Client Node deleted successfully"}
        return JsonResponse(data)