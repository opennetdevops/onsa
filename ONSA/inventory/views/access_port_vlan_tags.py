from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import VlanTag, AccessPort

import json

class AccessPortVlanTagsView(View):
    def get(self, request, accessport_id):
        access_port = AccessPort.objects.get(pk=accessport_id)
        used = request.GET.get('used')
        
        if used == "true":
            all_vlans = VlanTag.objects.filter(accessPorts=access_port).values()
        elif used == "false":
            all_vlans = VlanTag.objects.exclude(accessPorts=access_port).values()
        else:
            all_vlans = VlanTag.objects.all().values()
        return JsonResponse(list(all_vlans), safe=False)

    def post(self, request, accessport_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        access_port = AccessPort.objects.get(pk=accessport_id)
        vlan_tag = data['vlan_tag'] 
        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        vlan_tag.accessPorts.add(access_port)
        vlan_tag.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, accessport_id, vlan_tag):
        access_port = AccessPort.objects.get(pk=accessport_id)
        vlan_tag = VlanTag.objects.get(vlan_tag=vlan_tag)
        vlan_tag.accessPorts.remove(access_port)
        vlan_tag.save()
        data = {"Message" : "VlanTag deleted successfully from access port"}
        return JsonResponse(data, safe=False)
