from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from enum import Enum
import json
import requests
from pprint import pprint



class ServiceView(View):

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		url = settings.JEAN_GREY_URL + "brownfield/services"
		rheaders = { 'Content-Type': 'application/json' }
		response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)