from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.views import View
import json
import requests

class VlansView(View):

    def get(self, request):
        quantity = requests.GET.get("quantity")

        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(settings.INVENTORY_URL, auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)

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

class LogicalUnitsView(View):
    def get(self, request):
       pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class IpamView(View):
    def get(self, request):
       pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class AccessPortsView(View):
    def get(self, request):
       pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class LocationsView(View):
    def get(self, request):
        rheaders = {'Content-Type': 'application/json'}
        response = requests.get(settings.INVENTORY_URL + "locations", auth = None, verify = False, headers = rheaders)
        json_response = json.loads(response.text)

        return JsonResponse(json_response, safe=False)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass