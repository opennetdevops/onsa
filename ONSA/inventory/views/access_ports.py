from django.core import serializers
from django.http import HttpResponse
from django.views import View

from ..models import Location, AccessNode

import json

class AccessPortsView(View):
	def get(self, request, accessnode_id):
		access_node = AccessNode.objects.get(pk=accessnode_id)
		access_ports = access_node.get_access_ports_from_node()
		
		data = serializers.serialize('json', access_ports)
		return HttpResponse(data, content_type='application/json')

	def post(self, request, accessnode_id, accessport_num):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_node = AccessNode.objects.get(pk=accessnode_id)

		access_port = AccessPorts.objects.create(**data, location=location)
		access_port.save()
		access_port = AccessPorts.objects.filter(port=accessport_num)
		
		data = serializers.serialize('json', access_port)
		return HttpResponse(data, content_type='application/json')

	def put(self, request, accessnode_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_node = AccessNode.objects.filter(pk=accessnode_id)
		access_node.update(**data)

		data = serializers.serialize('json', access_node)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request, accessnode_id):
		access_node = AccessNode.objects.filter(pk=accessnode_id)
		access_node.delete()
		
		data = '{"Message" : "AccessNode deleted successfully"}'
		return HttpResponse(data, content_type='application/json')