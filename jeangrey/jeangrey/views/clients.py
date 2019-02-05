from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from jeangrey.models import Client, CustomerLocation, Service
from jeangrey.utils import *
from jeangrey.forms import *

import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class ClientView(View):

	def get(self, request, client_id=None):
		try:
			if client_id is None:
				name = request.GET.get('name', None)
				if name is None:
					s = Client.objects.all().values()
					return JsonResponse(list(s), safe=False)
				else:
					s = Client.objects.get(name=name)
					json_response = s.fields()
					return JsonResponse(json_response, safe=False)
			else:
				s = Client.objects.get(pk=client_id)
				json_response = s.fields()
				return JsonResponse(json_response, safe=False)

		except Client.DoesNotExist as e:
			logging.error(e)
			return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)
		

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		form = ClientForm(data)

		if form.is_valid():
			client = Client.objects.create(**data)
			client.save()
			response = {"message" : "Client requested"}
			return JsonResponse(response, safe=False, status=HTTP_201_CREATED)
		else:
			json_response = {"msg": "Form is invalid.", "errors": form.errors}

			return JsonResponse(json_response, safe=False, status=ERR_BAD_REQUEST)

	def put(self, request, client_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		form = ClientForm(data)

		try:
			if form.is_valid():
				client = Client.objects.get(pk=client_id)
				client.update(**data)

				json_response = Client.objects.filter(pk=client_id).values()

				return JsonResponse(json_response, safe=False)
			else:
				json_response = {"msg": "Form is invalid.", "errors": form.errors}

				return JsonResponse(json_response, safe=False, status=ERR_BAD_REQUEST)

		except Client.DoesNotExist as msg:
			logging.error(msg)
			return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)           

	def delete(self, request, client_id):
		try:
			client = Client.objects.get(pk=client_id)
			client.delete()

			return HttpResponse(status=HTTP_NO_CONTENT)

		except Client.DoesNotExist as msg:
			logging.error(msg)
			
			return JsonResponse({"msg": str(msg)}, safe=False, status=ERR_NOT_FOUND)