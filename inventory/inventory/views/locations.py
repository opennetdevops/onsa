from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from ..models import Location

import json

class LocationsView(View):
    
    def get(self, request, location_id=None):
        
        if location_id is None:
            name = request.GET.get('name', None)
            
            if name is not None:
                location = Location.objects.filter(name=name).values()
                response = location[0] if len(location) else []
                return JsonResponse(response, safe=False)
            else:
                locations = Location.objects.all().values()
                return JsonResponse(list(locations),safe=False)
            
        else:
            location = Location.objects.filter(pk=location_id).values()[0]   
            return JsonResponse(location, safe=False)

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