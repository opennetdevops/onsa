from django.core import serializers
from django.http import HttpResponse
from django.views import View

from ..models import VlanTag, AccessPort

import json

class VlanTagsView(View):
	def get(self, request, accessport_id):
		access_port = AccessPort.objects.filter(pk=accessport_id)
		vlan_tags = access_port.get_vlan_tags()
		
		data = serializers.serialize('json', vlan_tags)
		return HttpResponse(data, content_type='application/json')

	def post(self, request, accessport_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_port = AccessPort.objects.get(pk=accessnode_id)

		vlan_tag = VlanTag.objects.create(**data, accessPorts=access_port)
		vlan_tag.save()
		vlan_tag = VlanTag.objects.filter(vlan_tag=data['vlan_tag'])
		
		data = serializers.serialize('json', vlan_tag)
		return HttpResponse(data, content_type='application/json')

	def put(self, request, vlantag_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		vlan_tag = VlanTag.objects.filter(pk=vlantag_id)
		vlan_tag.update(**data)

		data = serializers.serialize('json', vlan_tag)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request, accessnode_id):
		vlan_tag = VlanTag.objects.filter(pk=accessnode_id)
		vlan_tag.delete()
		
		data = '{"Message" : "AccessNode deleted successfully"}'
		return HttpResponse(data, content_type='application/json')