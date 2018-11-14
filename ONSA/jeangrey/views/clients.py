from django.core import serializers
from django.http import JsonResponse
from django.views import View
from jeangrey.models.models import Client, CustomerLocation
import json


class ClientView(View):

    def get(self, request, client_id=None):
        if client_id is None:
            name = request.GET.get('name', None)
            if name is None:
                s = Client.objects.all().values()
                return JsonResponse(list(s), safe=False)
            else:
                s = Client.objects.filter(name=name).values()[0]
                return JsonResponse(s, safe=False)
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

    def delete(self, request, client_id):
        client = Client.objects.filter(pk=client_id)
        client.delete()
        data = {"Message" : "Client deleted successfully"}
        return JsonResponse(data)



class CustomerLocationView(View):

    def get(self, request, client_id, customer_location_id=None):
        if customer_location_id is None:
            data = CustomerLocation.objects.filter(client_id=client_id).values()
            return JsonResponse(list(data), safe=False)
        else:
            data = CustomerLocation.objects.filter(pk=customer_location_id).values()[0]
            return JsonResponse(data, safe=False)
        

    def post(self, request, client_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        data['client_id'] = client_id
        cl = CustomerLocation.objects.create(**data)
        cl.save()
        response = {"message" : "CustomerLocation requested"}
        return JsonResponse(response)

    def put(self, request, client_id, customer_location_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        cl = CustomerLocation.objects.get(pk=client_id).customer_location
        cl.update(**data)
        return JsonResponse(data, safe=False)

    def delete(self, request, client_id, customer_location_id):
        #TODO
        pass

