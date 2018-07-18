import jinja2
from .edge import *

import ipaddress

class NsxHandler(object):

	def create_edge(self, params):
		edge_params = {
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

		pprint(edge_params)

		return nsx_edge_create(edge_params)

	def add_gateway(self, edge_name):
		edge_id = nsx_edge_get_id_by_name(edge_name)
		return nsx_edge_add_gateway(edge_id, "0", "100.64.0.1", "1500")
	



