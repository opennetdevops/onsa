from django.core import serializers
from django.http import JsonResponse
from django.views import View
from jeangrey.models.models import Client, CustomerLocation
import json


class ClientView(View):

    def get(self, request, client_id=None):
        if client_id is None:
            s = Client.objects.all().values()
            return JsonResponse(list(s), safe=False)
        else:
            s = Client.objects.filter(pk=client_id).values()[0]
            return JsonResponse(s, safe=False)
        

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client = Client.objects.create(**data)
        client.save()
        response = {"message" : "Client requested"}
        return JsonResponse(response)

    def put(self, request, client_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        client = Client.objects.get(pk=client_id)
        client.update(**data)
        return JsonResponse(data, safe=False)



class CustomerLocationView(View):

    def get(self, request, client_id):
        cl = Client.objects.get(pk=client_id).customer_location
        data = CustomerLocation.objects.filter(pk=cl.id)
        return JsonResponse(data, safe=False)
        

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        cl = CustomerLocation.objects.create(**data)
        cl.save()
        response = {"message" : "CustomerLocation requested"}
        return JsonResponse(response)

    def put(self, request, client_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        cl = CustomerLocation.objects.get(pk=client_id).customer_location
        cl.update(**data)
        return JsonResponse(data, safe=False)

