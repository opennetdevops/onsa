from django.http import JsonResponse
from django.views import View
from inventory.models import VlanTag, AccessPort
from inventory.constants import *
from inventory.exceptions import *

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class VlanTagsView(View):
    def get(self, request):
        return JsonResponse(list(VlanTag.objects.all().values()), safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        vlan_tag = VlanTag.objects.create(**data)
        vlan_tag.save()
        vlan_tag = VlanTag.objects.filter(vlan_tag=data["vlan_tag"]).values()[0]
        return JsonResponse(vlan_tag, safe=False, status=HTTP_201_CREATED)

    def delete(self, request, vlan_tag_id):
        try:
            vlan_tag = VlanTag.objects.filter(pk=vlan_tag_id)
            my_vlan_tag = vlan_tag.values()[0]
            vlan_tag.delete()
            data = {"Message" : "VlanTag Pod deleted successfully"}
            return JsonResponse(data, status=HTTP_204_NO_CONTENT)
        except IndexError:
            msg = "VlanTag not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
