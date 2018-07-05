from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import Location

import json

class LocationsView(View):

	def get(self, request):
		locations = Location.objects.all()

		if request.content_type == 'application/json':
			data = serializers.serialize('json', locations)
			return HttpResponse(data, content_type='application/json')

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		location = Location.objects.create(**data)
		location.save()
		location = Location.objects.filter(name=data['name'])

		if request.content_type == 'application/json':
			data = serializers.serialize('json', location)
			return HttpResponse(data, content_type='application/json')

	def put(self, request, location_id):
		pass

	def delete(self, request, location_id):
		pass