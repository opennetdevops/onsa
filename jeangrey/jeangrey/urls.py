from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from jeangrey.views import services, clients

urlpatterns = [
	
	path('/api/clients', require_http_methods(["GET","POST"])(clients.ClientView.as_view())),
    path('/api/clients/<str:client_id>', require_http_methods(["GET", "PUT", "DELETE"])(clients.ClientView.as_view())),
	path('/api/clients/<str:client_id>/customerlocations', require_http_methods(["GET", "POST"])(clients.CustomerLocationView.as_view())),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>', require_http_methods(["GET","PUT", "DELETE"])(clients.CustomerLocationView.as_view())),
    path('/api/services', require_http_methods(["GET", "POST"])(services.ServiceView.as_view())),
	path('/api/services/<str:service_id>', require_http_methods(["GET", "PUT", "DELETE"])(services.ServiceView.as_view())),
	path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>/accessports', require_http_methods(["GET"])(clients.CustomerLocationAccessPortsView.as_view())),
	
 ]