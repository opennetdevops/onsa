from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from .views import devices, portgroups, virtualpods, locations, router_nodes, access_nodes, access_ports
from .views import router_node_logical_units, logical_units, location_access_nodes, location_router_nodes
from .views import access_node_access_ports, location_access_ports, access_node_vlan_tags, locations_virtual_pod
from .views import virtualpod_portgroups, client_nodes, vlan_tags, client_node_client_ports, client_node_ports, vrf

urlpatterns = [ 
    path('/api/login', obtain_jwt_token),
    path('/api/devices', devices.devices),
    
    path('/api/locations', require_http_methods(["GET","POST"])(locations.LocationsView.as_view())),
    path('/api/locations/<int:location_id>', require_http_methods(["PUT","DELETE"])(locations.LocationsView.as_view())),
    path('/api/locations/<int:location_id>/routernodes', require_http_methods(["GET","POST"])(location_router_nodes.LocationRouterNodesView.as_view())),
    path('/api/locations/<int:location_id>/accessnodes', require_http_methods(["GET","POST"])(location_access_nodes.LocationAccessNodesView.as_view())),
    path('/api/locations/<int:location_id>/accessports', require_http_methods(["GET"])(location_access_ports.LocationAccessPortsView.as_view())),

    path('/api/virtualpods', require_http_methods(["GET","POST"])(virtualpods.VirtualPodsView.as_view())),
    path('/api/virtualpods/<int:virtualpod_id>', require_http_methods(["GET","PUT", "DELETE"])(virtualpods.VirtualPodsView.as_view())),
    path('/api/locations/<int:location_id>/virtualpods', require_http_methods(["GET","POST"])(locations_virtual_pod.LocationVirtualPodView.as_view())),
    path('/api/virtualpods/<int:virtualpod_id>/portgroups', require_http_methods(["GET"])(virtualpod_portgroups.VirtualpodPortgroupsView.as_view())),
    
    path('/api/portgroups', require_http_methods(["GET","POST"])(portgroups.PortgroupView.as_view())),
    path('/api/portgroups/<int:portgroup_id>', require_http_methods(["GET","PUT", "DELETE"])(portgroups.PortgroupView.as_view())),
    
    path('/api/routernodes', require_http_methods(["GET","POST"])(router_nodes.RouterNodesView.as_view())),
    path('/api/routernodes/<int:routernode_id>', require_http_methods(["PUT","DELETE"])(router_nodes.RouterNodesView.as_view())),
    path('/api/routernodes/<int:routernode_id>/logicalunits', require_http_methods(["GET","POST"])(router_node_logical_units.RouterNodeLogicalUnitsView.as_view())),
    path('/api/routernodes/<int:routernode_id>/logicalunits/<int:logicalunit_id>', require_http_methods(["DELETE"])(router_node_logical_units.RouterNodeLogicalUnitsView.as_view())),
    
    path('/api/accessnodes', require_http_methods(["GET","POST"])(access_nodes.AccessNodesView.as_view())),
    path('/api/accessnodes/<int:accessnode_id>', require_http_methods(["GET","PUT","DELETE"])(access_nodes.AccessNodesView.as_view())),
    path('/api/accessnodes/<int:accessnode_id>/accessports', require_http_methods(["GET","POST"])(access_node_access_ports.AccessNodeAccessPortsView.as_view())),
    
    path('/api/accessports', require_http_methods(["GET"])(access_ports.AccessPortsView.as_view())),
    path('/api/accessports/<int:accessport_id>', require_http_methods(["GET","PUT","DELETE"])(access_ports.AccessPortsView.as_view())),
    path('/api/accessnodes/<int:access_node_id>/vlantags', require_http_methods(["GET","POST"])(access_node_vlan_tags.AccesNodeVlanTagsView.as_view())),
    path('/api/accessnodes/<int:access_node_id>/vlantags/<int:vlan_tag>', require_http_methods(["DELETE"])(access_node_vlan_tags.AccesNodeVlanTagsView.as_view())),

    path('/api/vlantags', require_http_methods(["GET","POST"])(vlan_tags.VlanTagsView.as_view())),

    path('/api/clientnodes', require_http_methods(["GET","POST"])(client_nodes.ClientNodesView.as_view())),
    path('/api/clientnodes/<str:client_node_sn>', require_http_methods(["GET","PUT", "DELETE"])(client_nodes.ClientNodesView.as_view())),
    path('/api/clientnodes/<str:client_node_sn>/clientports', require_http_methods(["GET","POST"])(client_node_client_ports.ClientNodeClientPortsView.as_view())),
    path('/api/clientnodes/<str:client_node_sn>/clientports/<int:client_port_id>', require_http_methods(["GET","PUT", "DELETE"])(client_node_client_ports.ClientNodeClientPortsView.as_view())),
    path('/api/clientnodes/clientports/<int:client_port_id>', require_http_methods(["GET","PUT","POST","DELETE"])(client_node_ports.ClientNodePortsView.as_view())),
    
    path('/api/logicalunits/<int:logicalunit_id>', require_http_methods(["PUT","DELETE"])(logical_units.LogicalUnitsView.as_view())),
    path('/api/logicalunits', require_http_methods(["GET","POST"])(logical_units.LogicalUnitsView.as_view())),

    path('/api/vrf', require_http_methods(["GET","POST"])(vrf.VrfView.as_view())),
    path('/api/vrf/<int:vrf_id>', require_http_methods(["GET","PUT","DELETE"])(vrf.VrfView.as_view())),

 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
