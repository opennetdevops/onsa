from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import VirtualVmwPod

import json

class VirtualPodsView(View):
    def get(self, request, virtualpod_id=None):
        if not virtualpod_id is None:
            if VirtualVmwPod.objects.filter(pk=virtualpod_id).count() is not 0:
                virtual_pods = VirtualVmwPod.objects.filter(pk=virtualpod_id).values()[0]
                return JsonResponse(virtual_pods, safe=False)
            else:
                return JsonResponse({'message':"Not found"}, status=404)

        virtual_pods = VirtualVmwPod.objects.all().values()
        return JsonResponse(list(virtual_pods), safe=False)


    def put(self, request, virtualpod_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        virtual_pod = VirtualVmwPod.objects.filter(pk=virtualpod_id)
        virtual_pod.update(**data)
        my_virtual_pod = virtual_pod.values()
        return JsonResponse(list(my_virtual_pod), safe=False)


    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        virtual_pod = VirtualVmwPod.objects.create(**data)
        virtual_pod.save()
        return JsonResponse(data, safe=False)


    def delete(self, request, virtualpod_id):
        virtual_pod = VirtualVmwPod.objects.filter(pk=virtualpod_id)
        virtual_pod.delete()
        data = {"Message" : "Virtual Pod deleted successfully"}
        return JsonResponse(data)