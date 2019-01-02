from django.core import serializers
from django.http import JsonResponse
from django.views import View

from ..models import VlanTag, AccessPort

import json

class VlanTagsView(View):
	def get(self, request):
		return JsonResponse(list(VlanTag.objects.all().values()), safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		vlan_tag = VlanTag.objects.create(**data)
		vlan_tag.save()

		return JsonResponse(data, safe=False)
