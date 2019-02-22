from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import ClientNodePort, ClientNode
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class ClientNodeClientPortsView(View):
    def get(self, request, client_node_sn, client_port_id=None):
        used = request.GET.get('used', '').capitalize()
        try:
            cn = ClientNode.objects.get(serial_number=client_node_sn)
            if client_port_id is None:
                if used is True:
                    client_ports = ClientNodePort.objects.filter(client_node=client_node_sn, used=used).values()                
                else:
                    client_ports = ClientNodePort.objects.filter(client_node=client_node_sn).values()               
                return JsonResponse(list(client_ports), safe=False)
            else:
                client_port = ClientNodePort.objects.filter(client_node=client_node_sn, pk=client_port_id).values()[0]
                return JsonResponse(client_port, safe=False)
        except IndexError:
            msg = "ClientNodePort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except ClientNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def put(self, request, client_node_sn, client_port_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            cn = ClientNode.objects.get(serial_number=client_node_sn)
            client_port = ClientNodePort.objects.filter(client_node=client_node_sn, pk=client_port_id)
            my_client_node = client_port[0]
            client_port.update(**data)
            my_client_node = client_port[0]
            my_client_node.save()
            return JsonResponse(list(client_port.values()), safe=False)
        except IndexError:
            msg = "ClientNodePort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except ClientNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request, client_node_sn):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        print(data)
        client_port = ClientNodePort.objects.create(**data, client_node_id=client_node_sn)

        client_port.save()
        client_port = ClientNodePort.objects.filter(interface_name=data['interface_name'],client_node_id=client_node_sn).values()[0]
        return JsonResponse(client_port, safe=False, status=HTTP_201_CREATED)


    def delete(self, request, client_node_sn, client_port_id):
        try:
            cn = ClientNode.objects.get(serial_number=client_node_sn)
            client_port = ClientNodePort.objects.filter(client_node=client_node_sn, pk=client_port_id)
            my_client_node = client_port[0]
            client_port.delete()
            data = {"Message" : "Client Node Port deleted successfully"}
            return JsonResponse(data,status=HTTP_204_NO_CONTENT)
        except ClientNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except IndexError:
            msg = "ClientNodePort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

