from django.http import JsonResponse
from django.views import View

from ..models import Products

import json

class ProductsView(View):
    def get(self, request, product_id=None):

        if accessnode_id is None:
            access_nodes = AccessNode.objects.all().values()
            return JsonResponse(list(access_nodes), safe=False)
        else:
            access_node = AccessNode.objects.filter(pk=accessnode_id).values()[0]   
            return JsonResponse(access_node, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        access_node_id = data['access_node_id']
        vlan_tag = data['vlan_tag']
        product_id = data['product_id']
        client_node_sn = data['client_node_sn']
        client_node_port = data['client_node_port']
        bandwidth = data['bandwidth']
        access_port_id = data['access_port_id']
        vrf_id = data['vrf_id']

        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        access_node = AccessNode.objects.get(pk=access_node_id)

        a = Products(vlantag=vlan_tag, access_node=access_node, product_id=product_id, 
            bandwidth=bandwidth, client_node_port=client_node_port, client_node_sn=client_node_sn, access_port_id=access_port_id, vrf_id=vrf_id)
        a.save()
        return JsonResponse(data, safe=False)

    def put(self, request, accessnode_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        access_node = AccessNode.objects.filter(pk=accessnode_id)
        access_node.update(**data)
        my_access_node = access_node.values()
        return JsonResponse(list(my_access_node), safe=False)


    def delete(self, request, accessnode_id):
        access_node = AccessNode.objects.filter(pk=accessnode_id)
        access_node.delete()
        
        data = {"Message" : "AccessNode deleted successfully"}
        return JsonResponse(data)