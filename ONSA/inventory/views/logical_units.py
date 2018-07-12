from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework import status


from ..models import LogicalUnit

import json

class LogicalUnitsView(View):
    def get(self, request):
        lus = LogicalUnit.objects.all().values()        
        return JsonResponse(list(lus))

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        logical_unit = LogicalUnit.objects.create(**data)
        logical_unit.save()
        return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)


    def put(self, request, logicalunit_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        logical_unit = LogicalUnit.objects.filter(pk=logicalunit_id)
        logical_unit.update(**data)

        data = serializers.serialize('json', logical_unit)
        return HttpResponse(data, content_type='application/json')

    def delete(self, request, logicalunit_id):
        logical_unit = LogicalUnit.objects.filter(pk=logicalunit_id)
        logical_unit.delete()
        
        data = '{"Message" : "Logical Unit deleted successfully"}'
        return HttpResponse(data, content_type='application/json')