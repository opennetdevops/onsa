from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils import *
from core.views.ldap_jwt import *

import json
import requests
import logging


class MultiClientAccessPortsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])

    def get(self, request):
        try:
            return JsonResponse(get_multiclient_access_ports(),safe=False)
        except BaseException as e:
            logging.error("exception")
            return e.handle()


multiclient_access_ports = MultiClientAccessPortsView.as_view()
