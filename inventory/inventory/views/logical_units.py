from django.core import serializers
from django.http import JsonResponse
from django.views import View
from inventory.constants import *
from inventory.exceptions import *
from inventory.models import LogicalUnit

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class LogicalUnitsView(View):
    def get(self, request, logicalunit_id=None):
        try:
            if logicalunit_id is None:
                lus = LogicalUnit.objects.all().values()        
                return JsonResponse(list(lus), safe=False)
            else:
                lu = LogicalUnit.objects.filter(pk=logicalunit_id).values()[0]        
                return JsonResponse(lu, safe=False)
        except IndexError:
            msg = "LogicalUnit not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)



    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        logical_unit = LogicalUnit.objects.create(**data)
        logical_unit.save()
        logical_unit = LogicalUnit.objects.filter(logical_unit_id=data["logical_unit_id"]).values()[0]
        return JsonResponse(logical_unit, status=HTTP_201_CREATED, safe=False)


    def put(self, request, logicalunit_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        try:
            logical_unit = LogicalUnit.objects.filter(pk=logicalunit_id)
            my_lu = logical_unit.values()[0]
            logical_unit.update(**data)
            my_lu = logical_unit.values()[0]
            return JsonResponse(my_lu,safe=False)
        except IndexError:
            msg = "LogicalUnit not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)


    def delete(self, request, logicalunit_id):
        try:
            logical_unit = LogicalUnit.objects.filter(pk=logicalunit_id)
            my_lu = logical_unit.values()[0]
            logical_unit.delete()
            data = '{"Message" : "LogicalUnit deleted successfully"}'
            return JsonResponse(data,safe=False)
        except IndexError:
            msg = "LogicalUnit not found."
            logging.error(msg)
            return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)

