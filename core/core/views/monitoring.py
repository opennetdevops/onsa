from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from core.utils import *
from core.utils.swagger import StatusMonitoringSerializer, ListQuerySerializer, TrafficSerializer
from core.views.ldap_jwt import *


import json
import requests

from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.utils import no_body, swagger_auto_schema

from rest_framework.decorators import api_view


class StatusMonitoringView(APIView):
    """ This class is created for documentation purpouses only.
    """
    # swagger_schema = None

    permission_classes = (IsAuthenticated,)
    authentication_classes = ([JSONWebTokenLDAPAuthentication, ])
    
    @swagger_auto_schema(
    query_serializer=ListQuerySerializer, # query params serializar
    responses={200: StatusMonitoringSerializer(many=True, help_text="List of dictionaries")},
    # response serializer 
    operation_description="Obtain the actual status of the device.", tags=['monitoring'],)
    
    def get(self, request, service_id=None):
        pass
        
status_monitoring_view = StatusMonitoringView.as_view()
