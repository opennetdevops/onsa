# from django.contrib import admin
# from django.conf import settings

from django.urls import path, reverse
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.decorators.http import require_http_methods
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.views import obtain_jwt_token

# Imports para drf_yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.views import *
from core.views.ldap_jwt import obtain_ldap_jwt_token
from core.views.ldap_jwt import *
from core.utils.swagger import swagger_info


# Swagger Schema View setup.
schema_view = get_schema_view(
    swagger_info,
    url="http://" + os.getenv('SERVER_IP') + ":8000/core",
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
    authentication_classes=([JSONWebTokenLDAPAuthentication, ]),
)
# Routes

urlpatterns = [
    path('/api/login', obtain_ldap_jwt_token),
    path('/api/services', require_http_methods(["GET", "POST"])(service_view)),
    path('/api/services/<str:service_id>',
         require_http_methods(["GET", "PUT","DELETE"])(service_view)),
    path('/api/services/<str:service_id>/activation',
         require_http_methods(["POST"])(service_activation_view)),
    path('/api/services/<str:service_id>/resources',
         require_http_methods(["GET"])(service_resources_view)),
    path('/api/clients', require_http_methods(["GET", "POST"])(client_view)),
    path('/api/clients/<str:client_id>',
         require_http_methods(["GET"])(client_view)),
    path('/api/clients/<str:client_id>/customerlocations',
         require_http_methods(["GET", "POST"])(customer_locations_view)),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>',
         require_http_methods(["GET"])(customer_locations_view)),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>/accessports',
         require_http_methods(["GET"])(client_customer_location_access_ports_view)),
    path('/api/locations',
         require_http_methods(["GET", "DELETE"])(locations_view)),
    path('/api/logicalunits',
         require_http_methods(["GET", "POST", "DELETE"])(logical_units_view)),
    path('/api/accessnodes/<str:access_node_id>/vlantags',
         require_http_methods(["GET", "POST", "DELETE"])(vlans_view)),
    path('/api/vrfs',
         require_http_methods(["GET", "PUT", "DELETE"])(vrfs_view)),
    path('/api/multiclient_access_ports',
         require_http_methods(["GET"])(multiclient_access_ports)),

    # Test for Monitoring

    path('/api/monitoring/<str:service_id>/status',
        require_http_methods(["GET"])(status_monitoring_view)),
    path('/api/monitoring/<str:service_id>/traffic',
        require_http_methods(["GET"])(traffic_monitoring_view)),



    # Swagger Routes
    url('/swagger', schema_view.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    url('/api', schema_view.with_ui('swagger', cache_timeout=0)),
    url('/api/docs', schema_view.with_ui('swagger', cache_timeout=0)),
    url('/docs', schema_view.with_ui('swagger', cache_timeout=0)),
]
