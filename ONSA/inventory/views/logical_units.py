from django.core import serializers
from django.http import HttpResponse
from django.views import View

from ..models import RouterNode, LogicalUnit

import json

class LogicalUnitsView(View):
	def get(self, request, routernode_id):
		router_node = RouterNode.objects.get(pk=routernode_id)
		lus = LogicalUnit.objects.all()
		print(lus)
		data = serializers.serialize('json', lus)
		print(data)

		all_lus = json.loads(data)
		updated_lus = []
		print("some")
		print(all_lus)		
		# for my_lu in all_lus:

		#     my_lu['fields']['used'] = last_type
		#     updated_lus.append(my_lu)

		
		return HttpResponse(data, content_type='application/json')

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		logical_unit = LogicalUnit.objects.create(**data)
		logical_unit.save()
		
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