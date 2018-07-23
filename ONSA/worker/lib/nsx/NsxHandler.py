import jinja2
from .nsx_rest import *
from ..common.render import render

from pprint import pprint

import ipaddress
import os

class NsxHandler(object):

	def _get_edge_id_by_name(name):
		r = nsxGet("/api/4.0/edges", "json")

		r_dict = json.loads(r)
	
		allEdges = r_dict['edgePage']['data']

		for edge in allEdges:
			if edge['name'] == name:
				return edge['id']

		return ""

	def _delete_by_id(edge_id):
		return nsxDelete("/api/4.0/edges/"+edgeId)

	def create_edge(self, params):

		"""
		Loading vars
		"""

		edge_vars = {
						"datacenterMoid" : params['datacenterMoid'],
						"name" : "VCPE-Test",
						"description" : "VCPE-Description",
						"appliances" : {
										"applianceSize" : "xlarge",
										"appliance" : {
														"resourcePoolId" : params['resourcePoolId'],
														"datastoreId" : params['datastoreId']
													}
										},
						"vnics" : [{"index" : "0",
									"name" : "Uplink",
									"type" : "Uplink",
									"portgroupId" : params['uplink']['portgroupId'],
									"primaryAddress" : params['uplink']['primaryAddress'],
									"subnetMask" : "255.255.254.0",
									"mtu" : "1500",
									"isConnected" : "true"},
									{"index" : "1",
									"name" : "Internal",
									"type" : "Internal",
									"portgroupId" : params['downlink']['portgroupId'],
									"primaryAddress" : list(ipaddress.ip_network(params['downlink']['public_cidr']).hosts())[0],
									"subnetMask" : "255.255.255.0",
									"mtu" : "1500",
									"isConnected" : "true"}],

						"cliSettings" : {"userName" : "admin",
										"password" : "T3stC@s3NSx!",
										"remoteAccess" : "true"}

					}

		dir = os.path.dirname(__file__)
		nsx_edge_xml = os.path.join(dir, '../../templates/edge/vcpe/create.j2')
		data = render(nsx_edge_xml, edge_vars)

		print(data)
  	
		status_code = nsxPost("/api/4.0/edges", data, "xml")

		return status_code

	def delete_edge(self, edge_name):
		edge_id = _get_edge_id_by_name(edge_name)
		status_code = _delete_by_id(edge_id)
		return status_code

	def add_gateway(self, edge_name):
		edge_id = _get_edge_id_by_name(edge_name)

		jinja_vars = {
						"description" : "description",
						"vnic" : "0",
						"gatewayAddress" : "100.64.0.1",
						"mtu" : "1500"
					}

		dir = os.path.dirname(__file__)
		nsx_static_json = os.path.join(dir, '../../templates/edge/vcep/irs/default_route.j2')
		data = render(nsx_static_json, jinja_vars) 

		status_code = nsxPut("/api/4.0/edges/" + edgeId + "/routing/config/static", data, "json")

		return status_code

	



