from django.core import serializers
from django.http import HttpResponse
from django.views import View

from ..models import Location, AccessNode

import json

class AccessNodesView(View):
	def get(self, request, location_id):
		location = Location.objects.get(pk=location_id)
		access_nodes = location.get_access_nodes()
		
		data = serializers.serialize('json', access_nodes)
		return HttpResponse(data, content_type='application/json')

	def post(self, request, location_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		location = Location.objects.get(pk=location_id)

		access_node = AccessNode.objects.create(**data, location=location)
		access_node.save()
		access_node = AccessNode.objects.filter(name=data['name'])
		
		data = serializers.serialize('json', access_node)
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