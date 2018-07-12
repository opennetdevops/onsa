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
        used = request.GET.get('used', '')
        
        if used == "true":
            all_lus = LogicalUnit.objects.filter(routerNodes=router_node).values()
        elif used == "false":
            all_lus = LogicalUnit.objects.exclude(routerNodes=router_node).values()
        else:
            all_lus = LogicalUnit.objects.all().values()
        return JsonResponse(list(all_lus), safe=False)
