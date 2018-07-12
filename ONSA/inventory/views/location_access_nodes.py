from django.http import JsonResponse
from django.views import View
from ..models import Location, AccessNode

import json

class LocationAccessNodesView(View):
    def get(self, request, location_id):
        access_nodes =  AccessNode.objects.filter(location_id=location_id).values()
        return JsonResponse(list(access_nodes), safe=False)
        


    def post(self, request, location_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        location = Location.objects.get(pk=location_id)

        access_node = AccessNode.objects.create(**data, location=location)
        access_node.save()
        access_node = AccessNode.objects.filter(name=data['name']).values()
        return JsonResponse(list(access_node), safe=False)