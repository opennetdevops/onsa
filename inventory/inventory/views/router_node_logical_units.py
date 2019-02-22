# Django imports
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from inventory.models import RouterNode, LogicalUnit
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class RouterNodeLogicalUnitsView(View):
    def get(self, request, routernode_id):
        try:
            router_node = RouterNode.objects.get(pk=routernode_id)
            used = request.GET.get('used', '').capitalize()
            
            if used == 'True':
                all_lus = LogicalUnit.objects.filter(router_nodes=router_node).values()
            elif used == 'False':
                all_lus = LogicalUnit.objects.exclude(router_nodes=router_node).values()
            else:
                all_lus = LogicalUnit.objects.all().values()
            return JsonResponse(list(all_lus), safe=False)
        except IndexError:
            msg = "RouterNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except RouterNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request, routernode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            router_node = RouterNode.objects.get(pk=routernode_id)
        except RouterNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        try:
            lu = LogicalUnit.objects.get(pk=data['logical_unit_id'])
        except LogicalUnit.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        if 'product_id' in data.keys():
            product_id = data['product_id'] 
            lu.product_id = product_id

        lu.router_nodes.add(router_node)
        lu.save()
        return JsonResponse(data, safe=False, status=HTTP_201_CREATED)


    def delete(self, request, routernode_id, logicalunit_id):
        try:
            router_node = RouterNode.objects.get(pk=routernode_id)
            lu = LogicalUnit.objects.get(logical_unit_id=logicalunit_id)
            my_lu = lu[0]
            lu.router_nodes.remove(router_node)
            lu.save()
            data = {"Message" : "RouterNode deleted successfully"}
            return JsonResponse(data, safe=False)
        except IndexError:
            msg = "LogicalUnit not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except RouterNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
            
