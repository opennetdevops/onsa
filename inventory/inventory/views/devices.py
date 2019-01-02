import json

from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# import sys
# sys.path.append("../")
from ..models import *



@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes((IsAuthenticated,))
def devices(request):
    locations = Location.objects.filter(name="CENTRO")
    VlanTag.initialize()
    routerNode = locations[0].get_router_node()
    print(routerNode)
    newAccessNode = AccessNode.add("AN", "1.1.1.1", "TN2020", 7, locations[0])
    pprint(newAccessNode)
    # pprint(newAccessNode.get_access_ports_from_node())
    access_port = newAccessNode.assign_free_access_port_from_node()
    print(access_port)
    print(access_port.get_free_vlans())
    print(access_port.get_used_vlans())
    vlan = access_port.assign_free_vlan()
    print("vlan: ",vlan)
    


    newAccessNode.delete()

    data = "{}"
    return JsonResponse(data)