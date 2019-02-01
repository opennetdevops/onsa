from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View
from inventory.constants import *
from inventory.exceptions import *
from inventory.models import Location

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class LocationsView(View):
    
    def get(self, request, location_id=None):       
        try:
            if location_id is None:
                name = request.GET.get('name', None)
                if name is not None:
                    location = Location.objects.filter(name=name).values()[0]
                    return JsonResponse(location, safe=False)
                else:
                    locations = Location.objects.all().values()
                    return JsonResponse(list(locations),safe=False)
                
            else: 
                location = Location.objects.filter(pk=location_id).values()[0]   
                return JsonResponse(location, safe=False)
        except IndexError:
            msg = "Location not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        location = Location.objects.create(**data)
        location.save()
        my_location = Location.objects.filter(name=data['name']).values()
        return JsonResponse(list(my_location), safe=False, status=HTTP_201_CREATED)

    def put(self, request, location_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            location = Location.objects.filter(pk=location_id)
            my_location = location.values()[0]
            location.update(**data)
            my_location = location.values()[0]
            return JsonResponse(my_location,safe=False)
        except IndexError:
            msg = "Location not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

    def delete(self, request, location_id):
        try:
            location = Location.objects.filter(pk=location_id)
            my_location = location.values()[0]
            location.delete()
            data = '{"Message" : "Location deleted successfully"}'
            return JsonResponse(data,safe=False)
        except IndexError:
            msg = "Location not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

