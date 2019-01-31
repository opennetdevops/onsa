# Django imports
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from rest_framework import status

# Python imports
import json

# ONSA imports
from inventory.models import VirtualVmwPod, Portgroup



class VirtualpodPortgroupsView(View):
    def get(self, request, virtualpod_id):
        try:
            virtual_pod = VirtualVmwPod.objects.get(pk=virtualpod_id)
        except ObjectDoesNotExist:
            return JsonResponse({'message':"Not found"}, status=404)

        used = request.GET.get('used', '').capitalize()
        
        if used == 'True':
            all_pgs = Portgroup.objects.filter(vmw_pod=virtual_pod, used=used).values()
        elif used == 'False':
            all_pgs = Portgroup.objects.filter(vmw_pod=virtual_pod, used=used).values()
        else:
            all_pgs = Portgroup.objects.filter(vmw_pod=virtual_pod).values()
        return JsonResponse(list(all_pgs), safe=False)
