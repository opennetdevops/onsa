from django.contrib import admin
from django.conf import settings

from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token
from core.views.ldap_jwt import obtain_ldap_jwt_token
from django.views.decorators.http import require_http_methods

from core.views import *

urlpatterns = [ 
    path('/api/login', obtain_ldap_jwt_token),
    path('/api/services', require_http_methods(["GET","POST"])(service_view)),
    path('/api/services/<str:service_id>', require_http_methods(["GET","PUT"])(service_view)),
    path('/api/services/<str:service_id>/activation', require_http_methods(["POST"])(service_activation_view)),
    path('/api/services/<str:service_id>/resources', require_http_methods(["GET"])(service_resources_view)),
    path('/api/clients', require_http_methods(["GET","POST"])(client_view)),
    path('/api/clients/<str:client_id>', require_http_methods(["GET"])(client_view)),
    path('/api/clients/<str:client_id>/customerlocations', require_http_methods(["GET", "POST"])(customer_locations_view)),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>', require_http_methods(["GET"])(customer_locations_view)),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>/accessports', require_http_methods(["GET"])(client_customer_location_access_ports_view)),
    path('/api/locations', require_http_methods(["GET","DELETE"])(locations_view)),
    path('/api/logicalunits', require_http_methods(["GET", "POST","DELETE"])(logical_units_view)),
    path('/api/accessnodes/<str:access_node_id>/vlantags', require_http_methods(["GET", "POST", "DELETE"])(vlans_view)),
    path('/api/vrfs', require_http_methods(["GET", "PUT", "DELETE"])(vrfs_view)),
]
