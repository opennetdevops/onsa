from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from enum import Enum
import json
import requests
from pprint import pprint

VRF_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls']
ALL_SERVICES = ['cpeless_mpls', 'cpe_mpls', 'vpls', 'projects', 'cpeless_irs', 'vcpe_irs', 'cpe_irs']
VPLS_SERVICES = ['vpls']
PROJECT_SERVICES = ['projects']

class ServiceView(View):

	def get(self, request, service_id=None):
		state = request.GET.get('state', None)
		service_type = request.GET.get('type', None)

		if service_id is not None:
			url = settings.JEAN_GREY_URL + "services/"+ str(service_id)
		else:
			url = settings.JEAN_GREY_URL + "services"

			if state is not None:
				url += "?state=" + state
			elif service_type is not None:
				url += "?type=" + service_type

		rheaders = { 'Content-Type': 'application/json' }
		response = requests.get(url, auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		url = settings.JEAN_GREY_URL + "services"
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

	def put(self, request, service_id):
		data = json.loads(request.body.decode(encoding='UTF-8'))
		service = Service.objects.filter(id=service_id)
		service.update(**data)
		return JsonResponse(data, safe=False)