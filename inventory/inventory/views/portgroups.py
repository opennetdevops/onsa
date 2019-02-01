from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.constants import *
from inventory.exceptions import *
from inventory.models import Portgroup

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class PortgroupView(View):
    def get(self, request, portgroup_id=None):
        try:
            if portgroup_id is not None:
                portgroups = Portgroup.objects.filter(pk=portgroup_id).values()[0]
                return JsonResponse(portgroups, safe=False)
            portgroups = Portgroup.objects.all().values()
            return JsonResponse(list(portgroups), safe=False)
        except IndexError:
            msg = "Portgroup not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def put(self, request, portgroup_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            portgroup = Portgroup.objects.filter(pk=portgroup_id)
            my_portgroup = portgroup.values()[0]
            portgroup.update(**data)
            my_portgroup = portgroup.values()[0]
            return JsonResponse(my_portgroup, safe=False)
        except IndexError:
            msg = "Portgroup not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        portgroup = Portgroup.objects.create(**data)
        portgroup.save()
        return JsonResponse(data, status=HTTP_201_CREATED, safe=False)


    def delete(self, request, portgroup_id):
        try:
            portgroup = Portgroup.objects.filter(pk=portgroup_id)
            my_portgroup = portgroup.values()[0]
            portgroup.delete()
            data = {"Message" : "Portgroup deleted successfully"}
            return JsonResponse(data)
        except IndexError:
            msg = "Portgroup not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)