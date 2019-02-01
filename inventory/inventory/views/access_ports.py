from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import AccessPort
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class AccessPortsView(View):
    def get(self, request, accessport_id=None):
        try:
            if accessport_id is None:
                access_ports = AccessPort.objects.all().values()
                return JsonResponse(list(access_ports), safe=False)
            else:
                access_port = AccessPort.objects.filter(pk=accessport_id).values()[0]   
                return JsonResponse(access_port, safe=False)
        except IndexError:
            msg = "AccessPort not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)




    def put(self, request, accessport_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            ap = AccessPort.objects.get(pk=accessport_id)
            access_port = AccessPort.objects.filter(pk=accessport_id)
            access_port.update(**data)
            my_access_port = access_port.values()
            
            return JsonResponse(list(my_access_port), safe=False)
        except AccessPort.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def delete(self, request, accessport_id):
        try:
            ap = AccessPort.objects.get(pk=accessport_id)
            access_port = AccessPort.objects.filter(pk=accessport_id)
            access_port.delete()
            data = {"Message" : "AccessPort deleted successfully"}
            return JsonResponse(data)
        except AccessPort.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)