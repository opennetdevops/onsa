from django.http import JsonResponse
from django.views import View

from ..models import Products, VlanTag, AccessNode

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


    def post(self, request, product_id=None):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        vlan_tag = data.pop('vlan_tag')
        access_node_id = data.pop('access_node_id')
        
        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        access_node = AccessNode.objects.get(pk=access_node_id)

        # data['access_node'] = access_node
        # data['vlan_tag'] = vlan_tag

        a = Products(**data,access_node=access_node,vlantag=vlan_tag  )
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