from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.models import VirtualVmwPod
from inventory.constants import *
from inventory.exceptions import *

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class VirtualPodsView(View):
    def get(self, request, virtualpod_id=None):
        try:
            if virtualpod_id is not None:
                virtual_pods = VirtualVmwPod.objects.filter(pk=virtualpod_id).values()[0]
            virtual_pods = VirtualVmwPod.objects.all().values()
            return JsonResponse(list(virtual_pods), safe=False)
        except IndexError:
            msg = "VirtualVmwPod not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def put(self, request, virtualpod_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            virtual_pod = VirtualVmwPod.objects.filter(pk=virtualpod_id)
            my_virtual_pod = virtual_pod.values()[0]
            virtual_pod.update(**data)
            my_virtual_pod = virtual_pod.values()[0]
            return JsonResponse(my_virtual_pod, safe=False)
        except IndexError:
            msg = "VirtualVmwPod not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        virtual_pod = VirtualVmwPod.objects.create(**data)
        virtual_pod.save()
        return JsonResponse(data, safe=False, status=HTTP_201_CREATED)


    def delete(self, request, virtualpod_id):
        try:
            virtual_pod = VirtualVmwPod.objects.filter(pk=virtualpod_id)
            my_virtual_pod = virtual_pod.values()[0]
            virtual_pod.delete()
            data = {"Message" : "Virtual Pod deleted successfully"}
            return JsonResponse(data)
        except IndexError:
            msg = "VirtualVmwPod not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)