from django.contrib import admin
from django.conf import settings

from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.http import require_http_methods

# from .views import service, pending_services, wrapper, projects, service_process
from .views import wrapper, service_activation, service

urlpatterns = [ 
    # url(r'^select2/', include('django_select2.urls')),
    # path('/api/login', obtain_jwt_token),
    path('/api/services', require_http_methods(["GET","POST"])(service.ServiceView.as_view())),
    path('/api/services/<str:service_id>', require_http_methods(["GET","PUT"])(service.ServiceView.as_view())),
    path('/api/services/<str:service_id>/activation', require_http_methods(["POST"])(service_activation.ServiceActivationView.as_view())),
    path('/api/services/<str:service_id>/resources', require_http_methods(["GET"])(service.ServiceResourcesView.as_view())),
    path('/api/clients', require_http_methods(["GET","POST"])(wrapper.ClientView.as_view())),
    path('/api/clients/<str:client_id>', require_http_methods(["GET"])(wrapper.ClientView.as_view())),
    path('/api/clients/<str:client_id>/customerlocations', require_http_methods(["GET", "POST"])(wrapper.CustomerLocationsView.as_view())),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>', require_http_methods(["GET"])(wrapper.CustomerLocationsView.as_view())),
    path('/api/clients/<str:client_id>/customerlocations/<str:customer_location_id>/accessports', require_http_methods(["GET"])(wrapper.ClientCustomerLocationAccessPortsView.as_view())),
    path('/api/locations', require_http_methods(["GET","DELETE"])(wrapper.LocationsView.as_view())),
    path('/api/logicalunits', require_http_methods(["GET", "POST","DELETE"])(wrapper.LogicalUnitsView.as_view())),
    path('/api/accessnodes/<str:access_node_id>/vlantags', require_http_methods(["GET", "POST", "DELETE"])(wrapper.VlansView.as_view())),
    path('/api/vrfs', require_http_methods(["GET", "PUT", "DELETE"])(wrapper.VrfsView.as_view())),

]
