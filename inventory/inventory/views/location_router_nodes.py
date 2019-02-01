from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from inventory.models import Location, RouterNode
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class LocationRouterNodesView(View):
    def get(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id)
            router_nodes = location.get_router_nodes().values()
            return JsonResponse(list(router_nodes),safe=False)
        except Location.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)