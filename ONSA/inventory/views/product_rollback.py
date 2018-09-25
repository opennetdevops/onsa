from django.http import JsonResponse
from django.views import View
from ..models import Products, LogicalUnit, Vrf, Portgroup
import json

class ProductRollbackView(View):



    def post(self, request, product_id):
        
        #Get product data
        my_product = Products.objects.filter(product_id=product_id).values()[0]

        #Clear Logical Units assigned (if any)
        my_logical_units = LogicalUnit.objects.filter(product_id=product_id).values()
        for my_lu in my_logical_units:
            my_lu.product_id = ""
            my_lu.save()

        #Clear portgroups assigned (if any)
        my_portgroups = Portgroup.objects.filter(product_id=product_id).values()
        for my_pg in my_portgroups:
            my_pg.product_id = ""
            my_pg.save()

        #Clear VRF in router_node (if any)
        #get location_id
        location_id = AccessNode.objects.get(pk=my_product.access_node_id).location_id
        #get all products with this VRF in this location
        my_products = Products.objects.filter(access_node_id__location_id=location_id, vrf_id=my_product.vrf_id).values()

        if ~my_products.count():
            my_vrf = Vrf.objects.get(rt=my_product.vrf_id)
            my_location = Location.objects.get(pk=location_id)
            my_vrf.locations.remove(my_location)

        #Clear model data
        my_product.client_node_sn = ""
        my_product.client_node_port = ""
        my_product.bandwidth = ""
        my_product.vrf_id = ""

        my_product.save()

        data = {"Message" : "Product rollback'd successfully"}
        return JsonResponse(data, safe=False)
