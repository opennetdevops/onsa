from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework import status

from ..models import VirtualVmwPod, Portgroup

import json


class VirtualpodPortgroupsView(View):
    def get(self, request, virtualpod_id):
        virtual_pod = VirtualVmwPod.objects.get(pk=virtualpod_id)
        used = request.GET.get('used')
        
        if used == "true":
            all_pgs = Portgroup.objects.filter(virtualVmwPod=virtual_pod, used=True).values()
        elif used == "false":
            all_pgs = Portgroup.objects.filter(virtualVmwPod=virtual_pod, used=False).values()
        else:
            all_pgs = Portgroup.objects.all().values()
        return JsonResponse(list(all_pgs), safe=False)
