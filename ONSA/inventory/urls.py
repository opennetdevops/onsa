from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from .views import devices, test_view, locations, router_nodes, access_nodes, access_ports, vlan_tags, logical_units

urlpatterns = [ 
    path('/api/login', obtain_jwt_token),
    path('/api/devices', devices.devices),
    path('/api/test', test_view.test),
    path('/api/locations', require_http_methods(["GET","POST"])(locations.LocationsView.as_view())),
    path('/api/locations/<int:location_id>', require_http_methods(["PUT","DELETE"])(locations.LocationsView.as_view())),
    path('/api/locations/<int:location_id>/routernodes', require_http_methods(["GET","POST"])(router_nodes.RouterNodesView.as_view())),
    path('/api/routernodes/<int:routernode_id>', require_http_methods(["PUT","DELETE"])(router_nodes.RouterNodesView.as_view())),
    path('/api/locations/<int:location_id>/accessnodes', require_http_methods(["GET","POST"])(access_nodes.AccessNodesView.as_view())),
    path('/api/accessnodes/<int:accessnode_id>', require_http_methods(["PUT","DELETE"])(access_nodes.AccessNodesView.as_view())),
    path('/api/accessnodes/<int:accessnode_id>/accessports', require_http_methods(["GET","POST"])(access_ports.AccessPortsView.as_view())),
    path('/api/accessports/<int:accessport_id>', require_http_methods(["PUT","DELETE"])(access_ports.AccessPortsView.as_view())),
    path('/api/accessports/<int:accessport_id>/vlantags', require_http_methods(["GET","POST"])(vlan_tags.VlanTagsView.as_view())),
    path('/api/vlantags/<int:vlantag_id>', require_http_methods(["PUT","DELETE"])(vlan_tags.VlanTagsView.as_view())),
    path('/api/routernodes/<int:routernode_id>/logicalunits', require_http_methods(["GET"])(logical_units.LogicalUnitsView.as_view())),
    path('/api/logicalunits/<int:logicalunit_id>', require_http_methods(["PUT","POST","DELETE"])(logical_units.LogicalUnitsView.as_view()))
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
