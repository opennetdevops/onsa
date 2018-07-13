from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import AccessPort

import json

class AccessPortsView(View):
	def get(self, request):
		access_ports = AccessPort.objects.all().values()
		return JsonResponse(list(access_ports), safe=False)