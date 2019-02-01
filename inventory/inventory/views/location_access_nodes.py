from django.http import JsonResponse
from django.views import View
from inventory.models import Location, AccessNode
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class LocationAccessNodesView(View):
    def get(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id)
            access_nodes =  AccessNode.objects.filter(location_id=location_id).values()
            return JsonResponse(list(access_nodes), safe=False)
        except Location.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request, location_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            location = Location.objects.get(pk=location_id)
            access_node = AccessNode.objects.create(**data, location=location)
            access_node.save()
            access_node = AccessNode.objects.filter(name=data['name']).values()
            return JsonResponse(list(access_node), safe=False, status=HTTP_201_CREATED)
        except Location.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)