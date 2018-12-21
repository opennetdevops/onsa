# Django imports
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework import status

# Python imports
import json

# ONSA imports
from inventory.models import RouterNode, LogicalUnit
from inventory.constants import *


class RouterNodeLogicalUnitsView(View):
    def get(self, request, routernode_id):
        try:
            router_node = RouterNode.objects.get(pk=routernode_id)
        except ObjectDoesNotExist:
                return HttpResponse(status=500)

        used = request.GET.get('used', '').capitalize()
        
        if used == 'True':
            all_lus = LogicalUnit.objects.filter(router_nodes=router_node).values()
        elif used == 'False':
            all_lus = LogicalUnit.objects.exclude(router_nodes=router_node).values()
            if list(all_lus) == []:
                return HttpResponse(status=ERR525)
        else:
            all_lus = LogicalUnit.objects.all().values()
        return JsonResponse(list(all_lus), safe=False)


    def post(self, request, routernode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        router_node = RouterNode.objects.get(pk=routernode_id)
        lu_id = data['logical_unit_id'] 
        product_id = data['product_id'] 
        lu = LogicalUnit.objects.get(logical_unit_id=lu_id)
        lu.product_id = product_id
        lu.router_nodes.add(router_node)
        lu.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, routernode_id, logicalunit_id):
        router_node = RouterNode.objects.get(pk=routernode_id)
        lu = LogicalUnit.objects.get(logical_unit_id=logicalunit_id)
        lu.router_nodes.remove(router_node)
        lu.save()
        data = {"Message" : "RouterNode deleted successfully"}
        return JsonResponse(data, safe=False)
