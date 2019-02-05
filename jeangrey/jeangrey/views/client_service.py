from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View

from jeangrey.models import Service, Client
from jeangrey.utils import *

import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class ClientServiceView(View):

	def get(self, request, client_id):
		service_type = request.GET.get('type', None)

		try:
			if service_type is not None:
				if service_type in ALL_SERVICES:
					json_response = Service.objects.filter(client=client_id, service_type=service_type).values()
			else:
				s = Service.objects.get(client=client_id)
				json_response = s.fields()

			return JsonResponse(json_response, safe=False)

		except Service.DoesNotExist as e:
			logging.error(e)
			return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)