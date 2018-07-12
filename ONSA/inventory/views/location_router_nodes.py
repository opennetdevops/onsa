from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import Location, RouterNode


import json


class LocationRouterNodesView(View):

    def get(self, request, location_id):
        location = Location.objects.get(pk=location_id)
        router_nodes = location.get_router_nodes().values()
        return JsonResponse(list(router_nodes),safe=False)
