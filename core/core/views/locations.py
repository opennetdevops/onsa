from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests

class LocationsView(APIView):
	def get(self, request):
		rheaders = {'Content-Type': 'application/json'}
		response = requests.get(settings.INVENTORY_URL + "locations", auth = None, verify = False, headers = rheaders)
		json_response = json.loads(response.text)

		return JsonResponse(json_response, safe=False)

locations_view = LocationsView.as_view()

