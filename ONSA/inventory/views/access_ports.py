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

	def post(self, request, accessnode_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_node = AccessNode.objects.get(pk=accessnode_id)

		access_port = AccessPort.objects.create(**data, accessNode=access_node)
		access_port.save()
		access_port = AccessPort.objects.filter(port=data['port'])
		
		data = serializers.serialize('json', access_port)
		return HttpResponse(data, content_type='application/json')

	def put(self, request, accessport_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_port = AccessPort.objects.filter(pk=accessport_id)
		access_port.update(**data)

		data = serializers.serialize('json', access_port)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request, accessport_id):
		access_port = AccessPort.objects.filter(pk=accessport_id)
		access_port.delete()
		
		data = '{"Message" : "AccessNode deleted successfully"}'
		return HttpResponse(data, content_type='application/json')