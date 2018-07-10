from django.core import serializers
from django.http import HttpResponse
from django.views import View

from ..models import RouterNode, LogicalUnit

import json

class LogicalUnitsView(View):
	def get(self, request, routernode_id):
		router_node = RouterNode.objects.get(pk=accessnode_id)
		router_nodes = router_node.get_access_ports_from_node()
		
		data = serializers.serialize('json', router_nodes)
		return HttpResponse(data, content_type='application/json')

	def post(self, request, routernode_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		router_node = RouterNode.objects.get(pk=accessnode_id)

		logical_unit = LogicalUnit.objects.create(**data, routerNodes=router_node)
		logical_unit.save()
		logical_unit = LogicalUnit.objects.filter(logical_unit_id=data['logical_unit_id'])
		
		data = serializers.serialize('json', logical_unit)
		return HttpResponse(data, content_type='application/json')

	def put(self, request, logicalunit_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		logical_unit = LogicalUnit.objects.filter(pk=logicalunit_id)
		logical_unit.update(**data)

		data = serializers.serialize('json', logical_unit)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request, logicalunit_id):
		logical_unit = LogicalUnit.objects.filter(pk=logicalunit_id)
		logical_unit.delete()
		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')