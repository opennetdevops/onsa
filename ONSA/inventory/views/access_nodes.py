from django.core import serializers
from django.http import HttpResponse
from django.views import View

from ..models import Location

class AccessNodesView(View):

	def get(self, request, node_id):
		
		if request.content_type == 'text/html':
			return HttpResponse()

		elif request.content_type == 'application/json':
			return JsonResponse("")

	def post(self, request, node_id):
		if request.content_type == 'text/html':
			pass
		elif request.content_type == 'application/json':
			data = serializers.serialize('json', router_nodes)
			return HttpResponse(data, content_type='application/json')
