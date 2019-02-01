from django.http import JsonResponse
from django.views import View
from inventory.models import VlanTag, AccessNode
from inventory.constants import *
from inventory.exceptions import *

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class AccesNodeVlanTagsView(View):
    def get(self, request, access_node_id):
        try:
            access_node = AccessNode.objects.get(pk=access_node_id)
            used = request.GET.get('used')
            
            if used == "true":
                all_vlans = VlanTag.objects.filter(access_nodes=access_node).values()
            elif used == "false":
                all_vlans = VlanTag.objects.exclude(access_nodes=access_node).values()
            else:
                all_vlans = VlanTag.objects.all().values()

            return JsonResponse(list(all_vlans), safe=False)
        except IndexError:
            msg = "AccessNode not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def post(self, request, access_node_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            access_node = AccessNode.objects.get(pk=access_node_id)
            vlan_tag = VlanTag.objects.get(vlan_tag=data['vlan_id'])
            vlan_tag.access_nodes.add(access_node)
            vlan_tag.save()
            
            return JsonResponse(data, safe=False, status=HTTP_201_CREATED)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def delete(self, request, access_node_id, vlan_tag):
        try:
            access_node = AccessNode.objects.get(pk=access_node_id)
        except AccessNode.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        try:
            vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        except VlanTag.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        vlan_tag.access_nodes.remove(access_node)
        vlan_tag.save()
        data = {"Message" : "VlanTag deleted successfully from access node"}
        return JsonResponse(data, safe=False)

