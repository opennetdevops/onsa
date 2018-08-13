import ipaddress

class VariablesHandler:

	def mx104_vcpeirs(params):
		bridge_domain_id = params['service_type'] + "-" + params['client_name']+ "-" + params["service_id"]

		params['bridge_domain_id'] = bridge_domain_id
		params['bridge_domain_description'] = "Description"
		params['vmw_interface_description'] = "Another description"
		params['an_interface_description'] = "Well, another one"

		return params


	def nsx_vcpe_irs(params):

		name = params['client_name']+"-"+params['service_id']

		new_params =  {}

		create_params = {
					"datacenterMoid" : params['datacenterMoid'],
					"name" : name,
					"description" : "vCPE-" + name,
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
								"primaryAddress" : params['uplink']['primaryAddress'].split("/")[0],
								"subnetMask" : "255.255.254.0",
								"mtu" : "1500",
								"isConnected" : "true"},
								{"index" : "1",
								"name" : "Internal",
								"type" : "Internal",
								"portgroupId" : params['downlink']['portgroupId'],
								"primaryAddress" : str(list(ipaddress.ip_network(params['downlink']['public_cidr']).hosts())[0]),
								"subnetMask" : str(ipaddress.ip_network(params['downlink']['public_cidr']).netmask),
								"mtu" : "1500",
								"isConnected" : "true"}],

					"cliSettings" : {"userName" : "admin",
									"password" : "T3stC@s3NSx!",
									"remoteAccess" : "true"}

				}

		gateway_params = {
						"description" : "description",
						"vnic" : "0",
						"gatewayAddress" : "100.64.0.1",
						"mtu" : "1500"
					}

		new_params['create_params'] = create_params
		new_params['gateway_params'] = gateway_params

		return new_params

	def s4224_vcpe_irs(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def s3290_5_vcpe_irs(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def mx104_cpeless_irs(params):
		pass

	def s4224_cpeless_irs(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def s3290_5_cpeless_irs(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def mx104_cpeless_mpls(params):
		pass

	def s4224_cpeless_mpls(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def s3290_5_cpeless_mpls(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def mx104_cpe_irs(params):
		pass

	def s4224_cpe_irs(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def mx104_cpe_mpls(params):
		pass

	def s4224_cpe_mpls(params):
		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']
		return params

	def mx104_vpls(params):
		pass

	def s4224_vpls(params):
		pass

	def s3290_5_vpls(params):
		pass