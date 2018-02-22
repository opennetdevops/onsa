import sys

from pprint import pprint
from .nsx_rest import *
from ..common.jinja import render

# from nsx_rest import *
# sys.path.append("../common/")
# from jinja import render

import json

# BGP_ROUTING
# TODO: definir que parametros de bgp se quieren tocar
def get_nsx_edge_bgp(edgeId):
	r = nsxGet("/api/4.0/edges/" + edgeId + "/routing/config/bgp")
	return json.loads(r)

def update_nsx_edge_bgp(edgeId, jinja_vars):
	dir = os.path.dirname(__file__)
	nsx_bgp_xml = os.path.join(dir, '../../templates/edge_routing/nsx_edge_routing_bgp.j2')
	data = render(nsx_bgp_xml, jinja_vars) 

	return nsxPost("/api/4.0/edges/" + edgeId + "/routing/config/bgp", data)

def delete_nsx_edge_bgp(edgeId):
	return nsxDelete("/api/4.0/edges/" + edgeId + "/routing/config/bgp")

# OSPF_ROUTING
# TODO: definir que parametros de ospf se quieren tocar
def get_nsx_edge_ospf(edgeId):
	r = nsxGet("/api/4.0/edges/" + edgeId + "/routing/config/ospf")
	return json.loads(r)

def update_nsx_edge_ospf(edgeId, jinja_vars):
	dir = os.path.dirname(__file__)
	nsx_ospf_xml = os.path.join(dir, '../../templates/edge_routing/nsx_edge_routing_ospf.j2')
	data = render(nsx_ospf_xml, jinja_vars) 

	return nsxPost("/api/4.0/edges/" + edgeId + "/routing/config/ospf", data)

def delete_nsx_edge_ospf(edgeId):
	return nsxDelete("/api/4.0/edges/" + edgeId + "/routing/config/ospf")

# STATIC_ROUTING
def get_nsx_edge_static(edgeId):
	r = nsxGet("/api/4.0/edges/" + edgeId + "/routing/config/static")
	return json.loads(r)

def update_nsx_edge_static(edgeId, jinja_vars):
	dir = os.path.dirname(__file__)
	nsx_static_xml = os.path.join(dir, '../../templates/edge_routing/nsx_edge_routing_static.j2')
	data = render(nsx_static_xml, jinja_vars) 

	print(data)

	return nsxPut("/api/4.0/edges/" + edgeId + "/routing/config/static", data)

def delete_nsx_edge_static(edgeId):
	return nsxDelete("/api/4.0/edges/" + edgeId + "/routing/config/static")

def nsx_edge_add_static_route(edgeId,
						  description,
						  vnic,
						  network,
						  nextHop,
						  mtu):

	jinja_vars = {'staticRouting' : {'staticRoutes' : {'route' : {'description' : description,
																  'vnic' : vnic,
																  'network' : network,
																  'nextHop' : nextHop,
																  'mtu' : mtu}}}}

	return update_nsx_edge_static(edgeId, jinja_vars)


def nsx_edge_add_gateway(edgeId, defaultRouteDescription, defaultRouteVnic, gatewayAddress, defaultRouteMtu):
	jinja_vars = {'staticRouting' : {'defaultRoute' : {'description': defaultRouteDescription,
									 				   'vnic' : defaultRouteVnic,
									 				   'gatewayAddress' : gatewayAddress,
									 				   'mtu' : defaultRouteMtu}}}

	pprint(jinja_vars)

	return update_nsx_edge_static(edgeId, jinja_vars)


def nsx_edge_add_static(edgeId, description, vnic, network, nextHop,
	mtu, defaultRouteDescription, defaultRouteMtu, defaultRouteVnic, gatewayAddress):

	jinja_vars = {'staticRouting' : {'staticRoutes' : {'route' : {'description' : description,
																  'vnic' : vnic,
																  'network' : network,
																  'nextHop' : nextHop,
																  'mtu' : mtu}},
									'defaultRoute' : {'description': defaultRouteDescription,
									 				   'vnic' : defaultRouteVnic,
									 				   'gatewayAddress' : gatewayAddress,
									 				   'mtu' : defaultRouteMtu}}}


	pprint(jinja_vars)

	return update_nsx_edge_static(edgeId, jinja_vars)


print(nsx_edge_add_static("edge-1774", "description", "0", "10.120.0.0/24", "191.12.12.1",
	"1500", "defaultRouteDescription", "1500", "0", "192.12.12.2").status_code)


# print(nsx_edge_add_static_route("edge-1774",
# 						  "description",
# 						  "0",
# 						  "10.10.10.0/24",
# 						  "192.168.0.1",
# 						  "1500").status_code)
# print(nsx_edge_add_gateway("edge-1774", "defaultRouteDescription", "0", "1.1.1.1", "1500").status_code)



