from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import Location, AccessNode, AccessPort
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class LocationAccessPortsView(View):
    def get(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id)
            access_nodes =  AccessNode.objects.filter(location_id=location_id)
            an = access_nodes[0]
            all_ports = []
            used = request.GET.get('used', '')

            for an in access_nodes:
                if used == "true":
                    my_ports = AccessPort.objects.filter(access_node=an, used=True).values()
                    for port in my_ports:
                        all_ports.append(port)
                elif used == "false":
                    my_ports = AccessPort.objects.filter(access_node=an, used=False).values()
                    for port in my_ports:
                        all_ports.append(port)
                else:
                    my_ports = AccessPort.objects.filter(access_node=an).values()
                    for port in my_ports:
                        all_ports.append(port)

            return JsonResponse(list(all_ports), safe=False)
        except Location.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except IndexError:
            msg = "AccessNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)