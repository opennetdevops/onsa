from django.http import JsonResponse
from django.views import View
from inventory.models import AccessNode
from inventory.constants import *
from inventory.exceptions import *

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class AccessNodesView(View):
    def get(self, request, accessnode_id=None):
        try:
            if accessnode_id is None:
                access_nodes = AccessNode.objects.all().values()
                return JsonResponse(list(access_nodes), safe=False)
            else:
                access_node = AccessNode.objects.filter(pk=accessnode_id).values()[0]   
                return JsonResponse(access_node, safe=False)
        except IndexError:
            msg = "AccessNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        access_node = AccessNode.objects.create(**data)
        access_node.save()
        access_node = AccessNode.objects.filter(name=data['name']).values()
        return JsonResponse(list(access_node), safe=False, status=HTTP_201_CREATED)

    def put(self, request, accessnode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            an = AccessNode.objects.get(pk=accessnode_id)    
            access_node = AccessNode.objects.filter(pk=accessnode_id)
            access_node.update(**data)
            my_access_node = access_node.values()
            return JsonResponse(list(my_access_node), safe=False)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def delete(self, request, accessnode_id):
        try:
            an = AccessNode.objects.get(pk=accessnode_id)  
            access_node = AccessNode.objects.filter(pk=accessnode_id)
            access_node.delete()
            data = {"Message" : "AccessNode deleted successfully"}
            return JsonResponse(data)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)