from django.http import JsonResponse
from django.views import View

from ..models import Products

import json

class ProductsView(View):
    def get(self, request, product_id=None):

        vrf = request.GET.get('vrf', '')

        if vrf:
            products = Products.objects.filter(vrf_id=vrf).values()
            return JsonResponse(list(products), safe=False)

        else:
            if product_id is None:
                products = Products.objects.all().values()
                return JsonResponse(list(products), safe=False)
            else:
                product = Products.objects.filter(product_id=product_id).values()[0]   
                return JsonResponse(product, safe=False)


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
        access_node = Products.objects.get(pk=access_node_id)

        a = Products(vlantag=vlan_tag, access_node=access_node, product_id=product_id, 
            bandwidth=bandwidth, client_node_port=client_node_port, client_node_sn=client_node_sn, access_port_id=access_port_id, vrf_id=vrf_id)
        a.save()
        return JsonResponse(data, safe=False)

    def put(self, request, product_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        product = Products.objects.filter(product_id=product_id)
        product.update(**data)
        my_product = product.values()[0]
        return JsonResponse(my_product, safe=False)


    def delete(self, request, product_id):
        product = Products.objects.filter(pk=product_id)
        product.delete()
        
        data = {"Message" : "Product deleted successfully"}
        return JsonResponse(data)