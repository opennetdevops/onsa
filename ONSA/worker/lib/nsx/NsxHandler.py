import jinja2
from .nsx_rest import *
from ..common.render import render

import requests

from pprint import pprint

import json

import ipaddress
import os


class NsxHandler(object):

	def _get_edge_id_by_name(name):
		rheaders = {'Accept': 'application/json'}

		r = requests.get(MANAGER + "/api/4.0/edges", auth=(USER, PASS), verify=False, headers=rheaders)

		r_dict = json.loads(r.text)	
		allEdges = r_dict['edgePage']['data']

		for edge in allEdges:
			if edge['name'] == name:
				return edge['id']

		return ""

	def _delete_by_id(edge_id):
		rheaders = {'Content-Type': 'application/xml'}
		r = requests.delete(MANAGER + "/api/4.0/edges/%s" % edge_id, auth =(USER, PASS), verify=False, headers=rheaders)

		return r.status_code

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
									"primaryAddress" : str(list(ipaddress.ip_network(params['downlink']['public_cidr']).hosts())[0]),
									"subnetMask" : "255.255.255.0",
									"mtu" : "1500",
									"isConnected" : "true"}],

						"cliSettings" : {"userName" : "admin",
										"password" : "T3stC@s3NSx!",
										"remoteAccess" : "true"}

					}

		"""
		Sending POST Operation
		"""

		dir = os.path.dirname(__file__)
		nsx_edge_xml = os.path.join(dir, '../../templates/edge/vcpe/irs/create.j2')
		data = render(nsx_edge_xml, edge_vars)

		# rheaders = {'Content-Type': 'application/xml'}
  		# r = requests.post(MANAGER + "/api/4.0/edges", data=data, auth=(USER, PASS), verify=False, headers=rheaders)
		status_code = 204
		return r.status_code, edge_vars

	def delete_edge(self, edge_name):
		edge_id = NsxHandler._get_edge_id_by_name(edge_name)
		status_code = NsxHandler._delete_by_id(edge_id)
		return status_code

	def add_gateway(self, edge_name):
		edge_id = NsxHandler._get_edge_id_by_name(edge_name)

		jinja_vars = {
						"description" : "description",
						"vnic" : "0",
						"gatewayAddress" : "100.64.0.1",
						"mtu" : "1500"
					}

		dir = os.path.dirname(__file__)
		nsx_static_json = os.path.join(dir, '../../templates/edge/vcpe/irs/default_route.j2')
		data = render(nsx_static_json, jinja_vars) 

		# rheaders = {'Content-Type': 'application/json'}
  		# r = requests.put(MANAGER + "/api/4.0/edges/%s" % edge_id, data=data, auth=(USER, PASS), verify=False, headers=rheaders)
		status_code = 201
		return status_code, jinja_vars

	



