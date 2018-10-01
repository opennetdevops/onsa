from django.contrib import admin
from django.conf import settings

from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.http import require_http_methods

from .views import service, client, client_service, pending_services, wrapper, projects


urlpatterns = [ 
    url(r'^select2/', include('django_select2.urls')),
    path('/api/login', obtain_jwt_token),
    path('/api/services', require_http_methods(["GET","POST"])(service.ServiceView.as_view())),
    path('/api/services/<str:service_id>', require_http_methods(["GET","PUT"])(service.ServiceView.as_view())),
    path('/api/clients', require_http_methods(["GET","POST"])(client.ClientView.as_view())),
    path('/api/clients/<int:client_id>', require_http_methods(["GET"])(client.ClientView.as_view())),
    path('/api/clients/<int:client_id>/services', require_http_methods(["GET"])(client_service.ClientServiceView.as_view())),
    path('/api/pending_services', require_http_methods(["GET","POST"])(pending_services.PendingServiceView.as_view())),
    path('/api/pending_services/<str:service_id>', require_http_methods(["GET","PUT"])(pending_services.PendingServiceView.as_view())),
    
    path('/api/locations', require_http_methods(["GET","DELETE"])(wrapper.LocationsView.as_view())),
    path('/api/products/<str:product_id>/accessports', require_http_methods(["GET", "POST","DELETE"])(wrapper.AccessPortsView.as_view())),
    path('/api/logicalunits', require_http_methods(["GET", "POST","DELETE"])(wrapper.LogicalUnitsView.as_view())),
    path('/api/accessnodes/<str:access_node_id>/vlantags', require_http_methods(["GET", "POST", "DELETE"])(wrapper.VlansView.as_view())),
    path('/api/vrfs', require_http_methods(["GET", "POST", "DELETE"])(wrapper.VrfsView.as_view())),
    path('/api/products', require_http_methods(["GET", "POST"])(projects.ProjectsView.as_view())),
    path('/api/products/<str:product_id>', require_http_methods(["GET", "PUT", "DELETE"])(projects.ProjectsView.as_view())),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
