from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import Location, RouterNode


import json

class RouterNodesView(View):

	def get(self, request):
		router_nodes = RouterNode.objects.all().values()
		return JsonResponse(list(router_nodes), safe=False)
		
		# data = serializers.serialize('json', router_nodes)
		# return HttpResponse(data, content_type='application/json')

	def post(self,request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		# location = Location.objects.get(pk=location_id)

		#todo check location
		router_node = RouterNode.objects.create(**data)
		router_node.save()
		router_node = RouterNode.objects.filter(name=data['name'])
		
		data = serializers.serialize('json', router_node)
		return HttpResponse(data, content_type='application/json')

	def put(self, request, routernode_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		router_node = RouterNode.objects.filter(pk=routernode_id)
		router_node.update(**data)

		data = serializers.serialize('json', router_nodes)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request, routernode_id):
		router_node = RouterNode.objects.filter(pk=routernode_id)
		router_node.delete()
		
		data = '{"Message" : "RouterNode deleted successfully"}'
		return HttpResponse(data, content_type='application/json')