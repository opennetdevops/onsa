from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import VlanTag, AccessNode, Services

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
        data = json.loads(request.body.decode(encoding='UTF-8'))
        
        vlan_tag = data['vlan_tag']
        service_id = data['service_id']
        client_node_sn = data['client_node_sn']
        client_node_port = data['client_node_port']
        bandwidth = data['bandwidth']
        access_port_id = data['access_port_id']

        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        access_node = AccessNode.objects.get(pk=access_node_id)

        a = Services(vlantag=vlan_tag, access_node=access_node, service_id=service_id, 
            bandwidth=bandwidth, client_node_port=client_node_port, client_node_sn=client_node_sn, access_port_id=access_port_id )
        a.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, access_node_id, vlan_tag):
        access_node = AccessNode.objects.get(pk=access_node_id)
        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        vlan_tag.access_nodes.remove(access_node)
        vlan_tag.save()
        data = {"Message" : "VlanTag deleted successfully from access node"}
        return JsonResponse(data, safe=False)
