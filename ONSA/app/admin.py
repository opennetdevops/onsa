from django.contrib import admin

from pprint import pprint
from .lib.utils.nsx.edge import *
from .lib.utils.nsx.edge_routing import *
from .lib.utils.vcenter import portgroups as vc_pg
from .lib.utils.juniper.mx_config import *
from .lib.utils.common.rest import *
from .models import *
from .forms import *
from ipaddress import *

from pprint import pprint

class NsxPublicIrsAdmin(admin.ModelAdmin):
	form = IrsServiceForm

	list_display = ('public_network','client','edge_name','hub', 'sco', 'sco_port', 'product_identifier')
	list_filter = ('client', 'edge_name')
	actions = ['delete_selected']

	exclude = ('public_network', 'edge_name', 'portgroup')

	def hub(self, obj):
		return obj.portgroup.hub

	def sco(self,obj):
		return obj.sco_port.sco


	def save_model(self, request, obj, form, change):

		obj.edge_name = "VCPE-" + obj.client.name + "-" + obj.product_identifier
				
		hub = form.cleaned_data['hub']
		sco = form.cleaned_data['sco']
		
		obj.portgroup = Portgroup.assign_free_pg_from_hub(form.cleaned_data['hub'])
		
		obj.ip_wan = IpWan.assign_free_wan_ip_from_hub(hub).network
		print("IP WAN: %s/32" % obj.ip_wan)
		
		obj.sco_port = ScoPort.assign_free_port_from_sco(form.cleaned_data['sco'])

		obj.public_network = IpPublicSegment.assign_free_public_ip()
		client_network = ip_network(obj.public_network.ip + "/" + str(obj.public_network.prefix))
		print("Public Network: ", client_network)
		print("Public Network Mask: ", client_network.netmask)
		print("Public Segment Gateway: %s/32" % list(client_network.hosts())[0])

		vxrail_logical_unit = LogicalUnit.assign_free_logical_unit_at_hub(form.cleaned_data['hub'])
		sco_logical_unit = LogicalUnit.assign_free_logical_unit_at_hub(form.cleaned_data['hub'])
		
		obj.vxrail_logical_unit = vxrail_logical_unit.logical_unit_id
		obj.sco_logical_unit = sco_logical_unit.logical_unit_id
		
		print("Uplink Portgroup Id: ", hub.uplink_pg_id)
		print("Public Portgroup Id: ", obj.portgroup.dvportgroup_id)

		jinja_vars = {  "datacenterMoid" : hub.datacenter_id,
						"name" : obj.edge_name, 
						"description" : "",
						"appliances" : {    "applianceSize" : 'xlarge',
																"appliance" : {"resourcePoolId" : hub.resource_pool_id,
																			 "datastoreId" : hub.datastore_id
																			}},
						"vnics" : [{"index" : "0",
										"name" : "uplink",
										"type" : "Uplink",
										"portgroupId" : hub.uplink_pg_id,
										"primaryAddress" : obj.ip_wan,
										"subnetMask" : "255.255.254.0", 
										"mtu" : "1500",
										"isConnected" : "true"
									},
									{"index" : "1",
										"name" : "public",
										"type" : "Internal",
										"portgroupId" : obj.portgroup.dvportgroup_id,
										"primaryAddress" : list(client_network.hosts())[0],
										"subnetMask" : client_network.netmask,
										"mtu" : "1500",
										"isConnected" : "true"
									 }],

						"cliSettings" : {"userName" : "admin",
										"password" : "T3stC@s3NSx!", #TODO: Change me
										"remoteAccess" : "true"}
				}

		pprint(jinja_vars)
		super(NsxPublicIrsAdmin, self).save_model(request, obj, form, change)
		
		# nsx_edge_create(jinja_vars)
		# edge_id = nsx_edge_get_id_by_name(obj.edge_name)
		# nsx_edge_add_gateway(edge_id, "0", "100.64.4.1", "1500") # CHANGE HARDCODED IP
		

		#load mx configuration parameters
		mx_parameters = {'mx_ip' : hub.mx_ip,
						'client_id' : "BD-" + obj.client.name + "-" + obj.product_identifier,
						'service_description' : "Public IRS Service",
						'vxrail_logical_unit' : obj.vxrail_logical_unit,
						'sco_logical_unit' : obj.sco_logical_unit,
						'vxrail_vlan' : obj.portgroup.vlan_tag,
						'sco_inner_vlan' : obj.sco_port.vlan_tag,
						'vxrail_description' : "VxRail CEN",
						'sco_description' : sco.name,
						'vxrail_ae_interface' : hub.vxrail_ae_interface,
						'sco_ae_interface': sco.sco_ae_interface,
						'sco_outer_vlan': sco.sco_outer_vlan,
						"public_network_ip" : client_network,
						"ip_wan" : obj.ip_wan}

		pprint(mx_parameters)
		# handler = NsxHandler()
		# handler.configure_mx(mx_parameters, "set")
		
	def delete_model(self, request, obj):
		
		# set portgroup to unused
		obj.portgroup.unassign()
		
		# set SCO port to unused
		obj.sco_port.unassign()

		# set logical units to unused
		LogicalUnit.unassign(obj.vxrail_logical_unit, obj.portgroup.hub)
		LogicalUnit.unassign(obj.sco_logical_unit, obj.portgroup.hub)

		# set Edge WAN IP to unused
		IpWan.unassign_ip(obj.ip_wan)

		# set public segment to unused
		obj.public_network.unassign()

		# delete edge
		nsx_edge_delete_by_name(obj.edge_name)

		# delete mx config

		# load mx configuration parameters
		mx_parameters = {'mx_ip' : obj.portgroup.hub.mx_ip,
						'client_id' : "BD-" + obj.client.name + "-" + obj.product_identifier,
						'vxrail_logical_unit' : obj.vxrail_logical_unit,
						'sco_logical_unit' : obj.sco_logical_unit,
						'vxrail_ae_interface' : obj.portgroup.hub.vxrail_ae_interface,
						'sco_ae_interface': obj.sco_port.sco.sco_ae_interface,
						"public_network_ip" : ip_network(obj.public_network.ip + "/" + \
											  str(obj.public_network.prefix))}

		pprint(mx_parameters)
		# NsxHandler.configure_mx(mx_parameters, "delete")
		obj.delete()

	def delete_selected(self, request, obj):
		# print("borrando selecteds!!")
		for o in obj.all():
			# set portgroup to unused
			o.portgroup.unassign()

			# set portgroup to unused
			o.sco_port.unassign()

			# set logical units to unused
			LogicalUnit.unassign(o.vxrail_logical_unit, o.portgroup.hub)
			LogicalUnit.unassign(o.sco_logical_unit, o.portgroup.hub)

			# set Edge WAN IP to unused
			IpWan.unassign_ip(o.ip_wan)

			# set public segment to unused
			o.public_network.unassign()

			# delete Edge
			nsx_edge_delete_by_name(o.edge_name)

			# delete MX config
			mx_parameters = {'mx_ip' : o.portgroup.hub.mx_ip,
						'client_id' : "BD-" + o.client.name + "-" + o.product_identifier,
						'vxrail_logical_unit' : o.vxrail_logical_unit,
						'sco_logical_unit' : o.sco_logical_unit,
						'vxrail_ae_interface' : o.portgroup.hub.vxrail_ae_interface,
						'sco_ae_interface': o.sco_port.sco.sco_ae_interface,
						"public_network_ip" : ip_network(o.public_network.ip + "/" + \
											  str(o.public_network.prefix))}


			NsxHandler.configure_mx(mx_parameters, "delete")


			# delete object
			o.delete()

class ClientAdmin (admin.ModelAdmin):
	list_display = ['name']

	def save_model(self, request, obj, form, change):
		super(ClientAdmin, self).save_model(request, obj, form, change)

class LogicalUnitAdmin(admin.ModelAdmin):
	list_display = ['logical_unit_id','used']


class PortgroupAdmin(admin.ModelAdmin):
	list_display = ['name','vlan_tag', 'hub', 'used']

class ScoPortAdmin(admin.ModelAdmin):
	list_display = ['description','port', 'sco', 'vlan_tag','used']

class IpWanAdmin(admin.ModelAdmin):
	list_display = ['network','prefix', 'hub','used']

class PublicNetworkAdmin(admin.ModelAdmin):
	list_display = ['ip','prefix','used']

class CpeLessIrsAdmin (admin.ModelAdmin):
	form = IrsServiceForm

	#exclude = ('edge_name', 'portgroup')
	list_display = ('public_network','client','hub', 'sco', 'sco_port', 'product_identifier')
	
	exclude = ['public_network']

	def hub(self, obj):
		return obj.hub

	def sco(self,obj):
		return obj.sco_port.sco

	def save_model(self, request, obj, form, change):
		
		hub = form.cleaned_data['hub']		
		sco = form.cleaned_data['sco']

		sco_port = ScoPort.assign_free_port_from_sco(form.cleaned_data['sco'])
		obj.sco_port = sco_port

		data = {"owner":"Public", "prefix":"29","hosts":"false"}
		# public_network = IpPublicSegment.assign_free_public_ip() # ToDo: get from FIPAM
		response = post("http://10.120.78.90/api/networks/assign_subnet", data,"json")
		obj.public_network = public_network
		client_network = ip_network(obj.public_network.ip + "/" + str(obj.public_network.prefix))

		print("Public Network: ", client_network)
		print("Public Network Mask: ", client_network.netmask)
		print("Public Segment Gateway: %s/32" % list(client_network.hosts())[0])

		sco_logical_unit = LogicalUnit.assign_free_logical_unit_at_hub(form.cleaned_data['hub'])
		
		obj.sco_logical_unit = sco_logical_unit.logical_unit_id
			
		super(CpeLessIrsAdmin, self).save_model(request, obj, form, change)
		
		#load mx configuration parameters
		mx_parameters = {'mx_ip' : hub.mx_ip,
						'client_id' : "CPELESS-" + obj.client.name + "-" + obj.product_identifier,
						'service_description' : "CPELess IRS Service", #ToDo: Define description with IDR
						'sco_logical_unit' : obj.sco_logical_unit,
						'sco_inner_vlan' : obj.sco_port.vlan_tag,
						'sco_description' : sco.name,
						'sco_ae_interface': sco.sco_ae_interface,
						'sco_outer_vlan': sco.sco_outer_vlan,
						"public_network_ip" : str(list(client_network.hosts())[0]) + "/" + str(obj.public_network.prefix),
						"vrf_name" : "INTERNET"}

		pprint(mx_parameters)

		handler = CpelessHandler()
		handler.configure_mx(mx_parameters, "set")

	def delete_model(self, request, obj):
		
		# set SCO port to unused
		obj.sco_port.unassign()

		# set logical units to unused
		LogicalUnit.unassign(obj.sco_logical_unit, obj.hub)

		# set public segment to unused
		obj.public_network.unassign()

		
		# load mx configuration parameters
		mx_parameters = {
						'mx_ip' : obj.hub.mx_ip,
						'sco_logical_unit' : obj.sco_logical_unit,
						'sco_ae_interface': obj.sco_port.sco.sco_ae_interface
						}

		pprint(mx_parameters)
		handler = CpelessHandler("irs")
		handler.configure_mx(mx_parameters, "delete")

		obj.delete()

class CpeLessMplsAdmin (admin.ModelAdmin):
	form = MplsServiceForm

	list_display = ('public_network','client','hub', 'sco', 'sco_port', 'product_identifier', 'vrf_name')
	exclude = ['public_network']

	def hub(self, obj):
		return obj.hub

	def sco(self,obj):
		return obj.sco_port.sco

	def save_model(self, request, obj, form, change):
		
		hub = form.cleaned_data['hub']		
		sco = form.cleaned_data['sco']

		sco_port = ScoPort.assign_free_port_from_sco(form.cleaned_data['sco'])
		obj.sco_port = sco_port

		public_network = IpPublicSegment.assign_free_public_ip() # ToDo: get from FIPAM
		obj.public_network = public_network
		client_network = ip_network(obj.public_network.ip + "/" + str(obj.public_network.prefix))

		print("Public Network: ", client_network)
		print("Public Network Mask: ", client_network.netmask)
		print("Public Segment Gateway: %s/32" % list(client_network.hosts())[0])

		sco_logical_unit = LogicalUnit.assign_free_logical_unit_at_hub(form.cleaned_data['hub'])
		
		obj.sco_logical_unit = sco_logical_unit.logical_unit_id
			
		super(CpeLessMplsAdmin, self).save_model(request, obj, form, change)
		
		#load mx configuration parameters
		mx_parameters = {'mx_ip' : hub.mx_ip,
						'client_id' : "CPELESS-" + obj.client.name + "-" + obj.product_identifier,
						'service_description' : "CPELess IRS Service", #ToDo: Define description with IDR
						'sco_logical_unit' : obj.sco_logical_unit,
						'sco_inner_vlan' : obj.sco_port.vlan_tag,
						'sco_description' : sco.name,
						'sco_ae_interface': sco.sco_ae_interface,
						'sco_outer_vlan': sco.sco_outer_vlan,
						"public_network_ip" : str(list(client_network.hosts())[0]) + "/" + str(obj.public_network.prefix),
						"vrf_name" : obj.vrf_name}

		pprint(mx_parameters)

		handler = CpelessHandler("mpls")
		handler.configure_mx(mx_parameters, "set")

	def delete_model(self, request, obj):
		
		# set SCO port to unused
		obj.sco_port.unassign()

		# set logical units to unused
		LogicalUnit.unassign(obj.sco_logical_unit, obj.hub)

		# set public segment to unused
		obj.public_network.unassign()

		
		# load mx configuration parameters
		mx_parameters = {
						'mx_ip' : obj.hub.mx_ip,
						'sco_logical_unit' : obj.sco_logical_unit,
						'sco_ae_interface': obj.sco_port.sco.sco_ae_interface,
						'vrf_name' : obj.vrf_name
						}

		pprint(mx_parameters)
		# handler = CpelessHandler("mpls")
		# handler.configure_mx(mx_parameters, "delete")

		obj.delete()

# Register
admin.site.register(Hub)
admin.site.register(Sco)
admin.site.register(LogicalUnit, LogicalUnitAdmin)
admin.site.register(IpWan,IpWanAdmin)
admin.site.register(IpPublicSegment, PublicNetworkAdmin)
admin.site.register(ScoPort,ScoPortAdmin)
admin.site.register(Portgroup,PortgroupAdmin)
admin.site.register(Client,ClientAdmin)
# admin.site.register(PrivateIrsService,PrivateIrsAdmin)
admin.site.register(NsxPublicIrsService,NsxPublicIrsAdmin)
admin.site.register(CpeLessIrsService,CpeLessIrsAdmin)
admin.site.register(CpeLessMplsService,CpeLessMplsAdmin)