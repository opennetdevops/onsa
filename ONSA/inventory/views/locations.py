from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import Location

import json

class LocationsView(View):
	
	def get(self, request):
		locations = Location.objects.all().values()
		return JsonResponse(list(locations),safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		location = Location.objects.create(**data)
		location.save()
		my_location = Location.objects.filter(name=data['name']).values()
		return JsonResponse(list(my_location), safe=False)

	def put(self, request, location_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		location = Location.objects.filter(pk=location_id)
		location.update(**data)
		my_location = location.values()
		return JsonResponse(list(my_location),safe=False)

	def delete(self, request, location_id):
		location = Location.objects.filter(pk=location_id)
		location.delete()
		
		data = '{"Message" : "Location deleted successfully"}'
		return JsonResponse(data,safe=False)