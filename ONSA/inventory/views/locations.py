from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import Location

class RouterNode(View):

	def get(self, request, location_name):

		location = Location.objects.get(name=location_name)
		router_node = location.get_router_node()

		if request.content_type == 'text/html':
			return HttpResponse()
		elif request.content_type == 'application/json':
			response = {"name" : str(router_node.name),
						"deviceType" : str(router_node.deviceType),
						"mgmtIP" : str(router_node.mgmtIP),
						"model" : str(router_node.model),
						"location" : router_node.location.name}


			return JsonResponse(response)

	def post(self,request, location_name):

		location = Location.objects.get(name=location_name)
		
		if request.content_type == 'text/html':
			return HttpResponse()
		elif request.content_type == 'application/json':

			return JsonResponse("")


class AccessNode(View):

	def get(self, request, **kwargs):
		if request.content_type == 'text/html':
			return HttpResponse()
		elif request.content_type == 'application/json':
			return JsonResponse("")

	def post(self, request, **kwargs):
		if request.content_type == 'text/html':
			return HttpResponse()
		elif request.content_type == 'application/json':
			return JsonResponse("")
