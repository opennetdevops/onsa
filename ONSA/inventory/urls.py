from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from .views import devices
from .views import test_view
from .views.locations import LocationsView 
from .views.router_nodes import RouterNodesView 
from .views.access_nodes import AccessNodesView


urlpatterns = [ 
    path('/api/login', obtain_jwt_token),
    path('/api/devices', devices.devices),
    path('/api/test', test_view.test),
    path('/api/locations', require_http_methods(["GET","POST"])(LocationsView.as_view())),
    path('/api/locations/<int:location_id>/routernodes', require_http_methods(["GET","POST"])(RouterNodesView.as_view())),
    path('/api/locations/<int:location_id>/routernodes/<int:routernode_id>', require_http_methods(["GET","PUT"])(RouterNodesView.as_view())),
    path('/api/locations/<int:location_id>/accessnode/<int:access_id>', require_http_methods(["GET","PUT"])(AccessNodesView.as_view()))
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
