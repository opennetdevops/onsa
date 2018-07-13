from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework import status

from ..models import RouterNode, LogicalUnit

import json


class RouterNodeLogicalUnitsView(View):
    def get(self, request, routernode_id):
        router_node = RouterNode.objects.get(pk=routernode_id)
        used = request.GET.get('used')
        
        if used == "true":
            all_lus = LogicalUnit.objects.filter(routerNodes=router_node).values()
        elif used == "false":
            all_lus = LogicalUnit.objects.exclude(routerNodes=router_node).values()
        else:
            all_lus = LogicalUnit.objects.all().values()
        return JsonResponse(list(all_lus), safe=False)


    def post(self, request, routernode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        router_node = RouterNode.objects.get(pk=routernode_id)
        lu_id = data['logical_unit_id'] 
        lu = LogicalUnit.objects.get(logical_unit_id=lu_id)
        lu.routerNodes.add(router_node)
        lu.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, routernode_id, logicalunit_id):
        router_node = RouterNode.objects.get(pk=routernode_id)
        lu = LogicalUnit.objects.get(logical_unit_id=logicalunit_id)
        lu.routerNodes.remove(router_node)
        lu.save()
        data = {"Message" : "RouterNode deleted successfully"}
        return JsonResponse(data, safe=False)
