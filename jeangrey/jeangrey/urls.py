from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from jeangrey.views import *

# Imports para drf_yasg 

# from rest_framework import permissions 
# from drf_yasg.views import get_schema_view 
# from drf_yasg import openapi 

# Swagger Schema View setup.
# schema_view = get_schema_view(
# 	openapi.Info( 
# 	title="ONSA - CORE API REST", 
# 	default_version='v1', 
# 	description="Documentation for REST API endpoints.", 
#     ),
# 	url="http://10.120.78.60:8002/jeangrey/api",
# 	public=True,
# 	permission_classes=(permissions.AllowAny,),
# 	)

urlpatterns = [
	
	path('/api/clients', require_http_methods(["GET","POST"])(clients.ClientView.as_view())),
    path('/api/clients/<str:client_id>', require_http_methods(["GET", "PUT", "DELETE"])(clients.ClientView.as_view())),
	path('/api/clients/<str:client_id>/customerlocations', require_http_methods(["GET", "POST"])(customer_locations.CustomerLocationView.as_view())),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>', require_http_methods(["GET","PUT", "DELETE"])(customer_locations.CustomerLocationView.as_view())),
    path('/api/services', require_http_methods(["GET", "POST"])(services.ServiceView.as_view())),
	path('/api/services/<str:service_id>', require_http_methods(["GET", "PUT", "DELETE"])(services.ServiceView.as_view())),
	path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>/accessports', require_http_methods(["GET"])(customer_locations_access_ports.CustomerLocationAccessPortsView.as_view())),
	]

# inclue this routes for swagger
	# url('/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
	# url('/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 

