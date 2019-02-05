from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from jeangrey.models import *
from jeangrey.utils import *
from jeangrey.forms import *

import jeangrey.models as models
import json
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class CustomerLocationView(View):

	def get(self, request, client_id, customer_location_id=None):

		try:
			c = Client.objects.get(pk=client_id)

			if customer_location_id is None:
				data = CustomerLocation.objects.filter(client_id=client_id).values()
				return JsonResponse(list(data), safe=False)
			else:
				cl = CustomerLocation.objects.get(pk=customer_location_id)
				data = cl.fields()
				return JsonResponse(data, safe=False) 

		except CustomerLocation.DoesNotExist as e:
			logging.error(e)
			return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)

	def post(self, request, client_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		data['client_id'] = client_id

		form = CustomerLocationForm(data)

		if form.is_valid():		
			cl = CustomerLocation.objects.create(**data)
			cl.save()
			return JsonResponse(cl.fields(), safe=False, status=HTTP_201_CREATED)
		else:
			msg = "Form is invalid."
			logging.error(msg)
			logging.error(form.errors)
			json_response = {"msg": msg, "errors": form.errors}
			return JsonResponse(json_response, safe=False, status=ERR_BAD_REQUEST)


	def put(self, request, client_id, customer_location_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		form = CustomerLocationForm(data)

		if form.is_valid():

			try:
				cl = CustomerLocation.objects.get(pk=client_id)
				cl.update(**data)

				data = CustomerLocation.objects.get(pk=client_id)

				return JsonResponse(data, safe=False)

			except CustomerLocation.DoesNotExist as e:
				logging.error(e)
				return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)

		else:
			json_response = {"msg": "Form is invalid.", "errors": form.errors}
			return JsonResponse(json_response, safe=False, status=ERR_BAD_REQUEST)
		

	def delete(self, request, client_id, customer_location_id):

		try:
			cl = CustomerLocation.objects.get(pk=customer_location_id)
			cl.delete()
			
			return HttpResponse(status_code=HTTP_204_NO_CONTENT)
			
		except CustomerLocation.DoesNotExist as e:
			logging.error(e)
			return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)