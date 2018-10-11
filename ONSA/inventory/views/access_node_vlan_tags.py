from django.http import JsonResponse
from django.views import View
from ..models import VlanTag, AccessNode, Products

import json

class AccesNodeVlanTagsView(View):
    def get(self, request, access_node_id):
        access_node = AccessNode.objects.get(pk=access_node_id)
        used = request.GET.get('used')
        
        if used == "true":
            all_vlans = VlanTag.objects.filter(access_nodes=access_node).values()
        elif used == "false":
            all_vlans = VlanTag.objects.exclude(access_nodes=access_node).values()
        else:
            all_vlans = VlanTag.objects.all().values()
        return JsonResponse(list(all_vlans), safe=False)

    def post(self, request, access_node_id):
        data = {"Message" : "Deprecated method"}

        return JsonResponse(data, safe=False)


    def delete(self, request, access_node_id, vlan_tag):
        access_node = AccessNode.objects.get(pk=access_node_id)
        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        vlan_tag.access_nodes.remove(access_node)
        vlan_tag.save()
        data = {"Message" : "VlanTag deleted successfully from access node"}
        return JsonResponse(data, safe=False)
