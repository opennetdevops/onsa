from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import Location, RouterNode
from inventory.constants import *
from inventory.exceptions import *

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class RouterNodesView(View):

    def get(self, request, routernode_id=None):
        try:
            if routernode_id is not None:
                router_nodes = RouterNode.objects.filter(id=routernode_id).values()[0]  
                return JsonResponse(router_nodes, safe=False)

            router_nodes = RouterNode.objects.all().values()
            return JsonResponse(list(router_nodes), safe=False)
        except IndexError:
            msg = "RouterNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)



    def post(self,request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        router_node = RouterNode.objects.create(**data)
        router_node.save()
        router_node = RouterNode.objects.filter(name=data['name']).values()[0]
        return JsonResponse(router_node, safe=False, status=HTTP_201_CREATED)


    def put(self, request, routernode_id):
        try:
            data = json.loads(request.body.decode(encoding='UTF-8'))
            router_node = RouterNode.objects.filter(pk=routernode_id)
            router_node.update(**data)
            my_router_node = router_node.values()[0]
            return JsonResponse(my_router_node, safe=False)
        except IndexError:
            msg = "RouterNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)        


    def delete(self, request, routernode_id):
        try:
            router_node = RouterNode.objects.filter(pk=routernode_id)
            my_router_node = router_node.values()[0]
            router_node.delete()
            router_node.delete()
            data = {"Message" : "RouterNode deleted successfully"}
            return JsonResponse(data, status=HTTP_204_NO_CONTENT)
        except IndexError:
            msg = "RouterNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
