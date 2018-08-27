from django.core import serializers
from django.http import JsonResponse
from django.views import View
from ..models import CpePort
import json


class CpePortsView(View):

    def get(self, request, client_node_id=None):
        if client_node_id is None:
            s = CpePort.objects.all().values()
        else:
            s = CpePort.objects.filter(cpe=client_node_id).values()
        return JsonResponse(list(s), safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        cpeport = CpePort.objects.create(**data)
        cpeport.save()
        response = {"message" : "CpePort requested"}
        return JsonResponse(response)

    def put(self, request, client_node_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        cpeport = CpePort.objects.get(pk=client_node_id)
        cpeport.update(**data)
        return JsonResponse(data, safe=False)