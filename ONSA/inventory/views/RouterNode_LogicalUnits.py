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
        lus = LogicalUnit.objects.all()
        
        data = serializers.serialize('json', lus)    
        all_lus = json.loads(data)
        updated_lus = []
        
        limit = request.GET.get('limit', '')
        used = request.GET.get('used', '')
        
        for my_lu in all_lus:
            if used == "true":
                if routernode_id in my_lu['fields']['routerNodes']:
                    my_lu['fields']['used'] = "True"
                    updated_lus.append(my_lu)
            elif used == "false":
                if routernode_id not in my_lu['fields']['routerNodes']:
                    my_lu['fields']['used'] = "False"
                    updated_lus.append(my_lu)
            else:
                return JsonResponse(all_lus, safe=False)         
        
        return JsonResponse(updated_lus, safe=False)
