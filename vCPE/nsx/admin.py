from django.contrib import admin
from pprint import pprint
from .lib.utils.nsx.edge import *
from .lib.utils.vcenter import GetPortgroups as vc_pg
from .lib.utils.juniper.MxConfig import *
from .models import *
from .forms import *




class PrivateIrsAdmin (admin.ModelAdmin):
	#exclude = ('edge_name', 'portgroup')
	list_display = ('ip_segment','client','edge_name')
	list_filter = ('client', 'edge_name')

	form = IrsServiceForm


class PublicIrsAdmin(admin.ModelAdmin):
	form = IrsServiceForm

	list_display = ('public_network','client','edge_name','hub', 'sco', 'sco_port')
	list_filter = ('client', 'edge_name')
	actions = ['delete_selected']


	exclude = ('public_network', 'edge_name', 'portgroup')

	def hub(self, obj):
		return obj.portgroup.hub

	def sco(self,obj):
		return obj.sco_port.sco


	def save_model(self, request, obj, form, change):

		#Create NSX Edge

		obj.edge_name = obj.client.name
		
		print("Hub Name: ",form.cleaned_data['hub'].name)
		hub = form.cleaned_data['hub']
		
		print("SCO Name: ",form.cleaned_data['sco'].name)
		sco = form.cleaned_data['sco']
		print("SCO Id: ",sco.sco_id)
		
		pg = Portgroup.assign_free_pg_from_hub(form.cleaned_data['hub'])
		print("Portgroup Name: ", pg.name)
		print("Portgroup used?: ", pg.used)
		obj.portgroup = pg
		
		wan_ip = IpWan.assign_free_wan_ip_from_hub(hub)
		obj.ip_wan = wan_ip.network
		print("IP Wan: ", obj.ip_wan)
		
		port = ScoPort.assign_free_port_from_sco(form.cleaned_data['sco'])
		print("Port Name: ", port.description)
		obj.sco_port = port

		public_network = IpPublicSegment.assign_free_public_ip()
		obj.public_network = public_network
		print("Public Network: ", obj.public_network.ip)



		
		uplink_portgroup_id = vc_pg.getPortgroupId(hub.uplink_pg)
		jinja_vars = {  "datacenterMoid" : hub.datacenter_id,
						"name" : 'Edge-Test-Django', #TODO: Change me
						"description" : "",
						"appliances" : {    "applianceSize" : 'xlarge',
																"appliance" : {"resourcePoolId" : hub.resource_pool_id,
																			 "datastoreId" : hub.datastore_id
																			}},
				"vnics" : [{"index" : "0",
										"name" : "uplink",
										"type" : "Uplink",
										"portgroupId" : uplink_portgroup_id,
										"primaryAddress" : "192.168.0.1", #TODO: Change me
										"subnetMask" : "255.255.254.0", #TODO: Change me
										"mtu" : "1500",
										"isConnected" : "true"
									 }],
				"cliSettings" : {"userName" : "admin",
												 "password" : "T3stC@s3NSx!", #TODO: Change me
												 "remoteAccess" : "true"}
				}

				#todo: add DG to NSX edge








		# print(form.cleaned_data)

		super(PublicIrsAdmin, self).save_model(request, obj, form, change)
		create_nsx_edge(jinja_vars)
		
		configure_vcpe_mx(form.cleaned_data['username'],
						  form.cleaned_data['password'],
						  hub.mx_ip,
						  "client_id",#todo change me
						  "service_description",#todo change me
						  "vxrail_log_unit",#todo change me
						  "sco_log_unit",#todo change me
						  obj.portgroup.vlan_tag, #vxrail_inner_vlan
						  obj.sco_port.vlan_tag,#sco_inner_vlan,
						  "vxrail_description",#todo change me
						  "sco_description",#todo change me
						  hub.vxrail_ae_interface,
						  sco.sco_ae_interface,
						  hub.vxrail_outer_vlan,
						  sco.sco_outer_vlan,
						  obj.public_network.ip, 
						  obj.ip_wan) 




	def delete_model(self, request, obj):
		print("borrando pg!!")
		obj.portgroup.unassign()
		print("borrando port!!")
		obj.sco_port.unassign()
		print("borrando ip!!")
		IpWan.unassign_ip(obj.ip_wan)
		obj.public_network.unassign()
		obj.delete()

	def delete_selected(self, request, obj):
		print("borrando selecteds!!")
		for o in obj.all():
			o.portgroup.unassign()
			o.sco_port.unassign()
			IpWan.unassign_ip(o.ip_wan)
			o.public_network.unassign()
			o.delete()





class ClientAdmin (admin.ModelAdmin):
	list_display = ['name']

	def save_model(self, request, obj, form, change):
		super(ClientAdmin, self).save_model(request, obj, form, change)

class PortgroupAdmin(admin.ModelAdmin):
	list_display = ['name','vlan_tag', 'hub', 'used']


class ScoPortAdmin(admin.ModelAdmin):
	list_display = ['description','port', 'sco', 'vlan_tag','used']


class IpWanAdmin(admin.ModelAdmin):
	list_display = ['network','prefix', 'hub','used']


class PublicNetworkAdmin(admin.ModelAdmin):
	list_display = ['ip','prefix','used']




admin.site.register(Hub)
admin.site.register(Sco)
admin.site.register(IpWan,IpWanAdmin)

admin.site.register(IpPublicSegment, PublicNetworkAdmin)

admin.site.register(ScoPort,ScoPortAdmin)
admin.site.register(Portgroup,PortgroupAdmin)
admin.site.register(Client,ClientAdmin)

admin.site.register(PrivateIrsService,PrivateIrsAdmin)
admin.site.register(PublicIrsService,PublicIrsAdmin)