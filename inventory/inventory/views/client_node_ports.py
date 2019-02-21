from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.constants import *
from inventory.exceptions import *
from inventory.models import ClientNodePort

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class ClientNodePortsView(View):
    def get(self, request, client_port_id=None):
        try:
            if client_port_id is not None:
                client_port = ClientNodePort.objects.filter(pk=client_port_id).values()[0]
                return JsonResponse(client_port, safe=False)
            else:
                client_ports = ClientNodePort.objects.all().values()
                return JsonResponse(list(client_ports), safe=False)
        except IndexError:
            msg = "ClientNodePort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def put(self, request, client_port_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            client_port = ClientNodePort.objects.filter(pk=client_port_id)
            my_client_node = client_port.values()[0]
            client_port.update(**data)
            my_client_node = client_port.values()[0]
            return JsonResponse(my_client_node, safe=False)
        except IndexError:
            msg = "ClientNodePort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)



    def delete(self, request, client_node_sn, client_port_id):
        try:
            client_port = ClientNodePort.objects.filter(client_node=client_node_sn)
            my_client_node = client_port.values()[0]
            client_port.delete()
            data = {"Message" : "Client Node Port deleted successfully"}
            return JsonResponse(data)
        except IndexError:
            msg = "ClientNodePort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
