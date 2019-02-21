from django.http import JsonResponse
from django.views import View
from inventory.constants import *
from inventory.exceptions import *
from inventory.models import Vrf, Location

import logging
import coloredlogs
import json

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class VrfLocationsView(View):
    def get(self, request, vrf_id, location_id=None):
        try:
            vrf = Vrf.objects.get(rt=vrf_id)
        except Vrf.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

        if location_id is not None:
            try:
                my_loc = Location.objects.get(pk=location_id)
            except Location.DoesNotExist as msg:
                logging.error(msg)
                return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

            exists = Vrf.objects.filter(rt=vrf_id, locations=location_id).values().count()
            data = {}
            if exists:
                data["exists"] = True
            else:
                data["exists"] = False
            return JsonResponse(data, safe=False)

        else:
            return JsonResponse(list(vrf.locations.all().values()), safe=False)


    def post(self, request, vrf_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            location = Location.objects.get(pk=location_id)
        except Location.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        try:
            vrf = Vrf.objects.get(rt=data['vrf_id'])
        except Vrf.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        vrf.locations.add(location)
        vrf.save()
        data = {"Message" : "Added location to vrf"}
        return JsonResponse(data, safe=False)


    def delete(self, request, vrf_id, location_id):
        try:
            my_vrf = Vrf.objects.get(rt=vrf_id)
        except Vrf.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)
        
        vrf = Vrf.objects.filter(rt=vrf_id)
        
        try:
            location = Location.objects.get(pk=location_id)
        except Location.DoesNotExist as msg:
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)        

        vrf.locations.remove(location)
        data = {"Message" : "Location deleted successfully from vrf"}
        return JsonResponse(data, safe=False)