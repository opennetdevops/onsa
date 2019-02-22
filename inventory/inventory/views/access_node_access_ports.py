from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from inventory.models import AccessPort, AccessNode
from inventory.constants import *
from inventory.exceptions import *
import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class AccessNodeAccessPortsView(View):
    def get(self, request, accessnode_id):
        try:
            used = request.GET.get('used', '').capitalize()
            access_port = AccessNode.objects.get(access_node=accessnode_id)
            if used == 'True':
                access_ports = AccessPort.objects.filter(access_node=accessnode_id,used=used).values()
            elif used == 'False':
                access_ports = AccessPort.objects.filter(access_node=accessnode_id,used=used).values()
            else:
                access_ports = AccessPort.objects.filter(access_node=accessnode_id).values()
            return JsonResponse(list(access_ports), safe=False)
        except IndexError:
            msg = "AccessNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request, accessnode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            access_node = AccessNode.objects.get(pk=accessnode_id)

            access_port = AccessPort.objects.create(**data, access_node=access_node)
            access_port.save()
            access_port = AccessPort.objects.filter(port=data['port']).values()[0]
            
            return JsonResponse(access_port, safe=False, status=HTTP_201_CREATED)
        except IndexError:
            msg = "AccessNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)