# Django imports
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import VirtualVmwPod, Portgroup
from inventory.constants import *
from inventory.exceptions import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class VirtualpodPortgroupsView(View):
    def get(self, request, virtualpod_id):
        try:
            virtual_pod = VirtualVmwPod.objects.get(pk=virtualpod_id)
        except VirtualVmwPod.DoesNotExist:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

        used = request.GET.get('used', '').capitalize()
        
        if used == 'True':
            all_pgs = Portgroup.objects.filter(vmw_pod=virtual_pod, used=used).values()
        elif used == 'False':
            all_pgs = Portgroup.objects.filter(vmw_pod=virtual_pod, used=used).values()
        else:
            all_pgs = Portgroup.objects.filter(vmw_pod=virtual_pod).values()
        return JsonResponse(list(all_pgs), safe=False)
