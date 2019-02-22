from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.constants import *
from inventory.exceptions import *
from inventory.models import ClientNode

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class ClientNodesView(View):
    def get(self, request, client_node_sn=None):
        try:
            if client_node_sn is not None:
                client_node = ClientNode.objects.filter(serial_number=client_node_sn).values()[0]
                return JsonResponse(client_node, safe=False)
            else:
                customer_location = request.GET.get('customer_location', None)
                if customer_location is not None:
                    client_nodes = ClientNode.objects.filter(customer_location=customer_location).values()
                else:
                    client_nodes = ClientNode.objects.all().values()
                return JsonResponse(list(client_nodes), safe=False)
        except IndexError:
            msg = "ClientNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)



    def put(self, request, client_node_sn):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            client_node = ClientNode.objects.filter(serial_number=client_node_sn)
            my_client_node = client_node.values()[0]
            client_node.update(**data)
            my_client_node = client_node.values()[0]
            return JsonResponse(my_client_node, safe=False)
        except IndexError:
            msg = "ClientNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client_node = ClientNode.objects.create(**data)
        client_node.save()
        client_node = ClientNode.objects.filter(name=data["name"]).values()[0]
        return JsonResponse(client_node, safe=False, status=HTTP_201_CREATED)


    def delete(self, request, client_node_sn):
        try:
            client_node = ClientNode.objects.filter(serial_number=client_node_sn)
            my_client_node = client_node.values()[0]
            client_node.delete()
            data = {"Message" : "Client Node deleted successfully"}
            return JsonResponse(data, status=HTTP_204_NO_CONTENT)
        except IndexError:
            msg = "ClientNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
            
