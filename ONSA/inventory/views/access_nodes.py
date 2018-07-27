from django.http import JsonResponse
from django.views import View

from ..models import AccessNode

import json

class AccessNodesView(View):
	def get(self, request, accessnode_id=None):

		if accessnode_id is None:
			access_nodes = AccessNode.objects.all().values()
			return JsonResponse(list(access_nodes), safe=False)
		else:
			access_node = AccessNode.objects.filter(pk=accessnode_id).values()[0]	
			return JsonResponse(access_node, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_node = AccessNode.objects.create(**data)
		access_node.save()
		access_node = AccessNode.objects.filter(name=data['name']).values()
		return JsonResponse(list(access_node), safe=False)

	def put(self, request, accessnode_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		access_node = AccessNode.objects.filter(pk=accessnode_id)
		access_node.update(**data)
		my_access_node = access_node.values()
		return JsonResponse(list(my_access_node), safe=False)


	def delete(self, request, accessnode_id):
		access_node = AccessNode.objects.filter(pk=accessnode_id)
		access_node.delete()
		
		data = {"Message" : "AccessNode deleted successfully"}
		return JsonResponse(data)