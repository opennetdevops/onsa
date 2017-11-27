from django.contrib import admin
from pprint import pprint
from .lib.utils.nsx.edge import *
from .lib.utils.vcenter.GetPortgroups import *
from .models import Hub, Portgroup, Client, PrivateIrsService, PublicIrsService

class PrivateIrsAdmin (admin.ModelAdmin):
	exclude = ('edge_name',)
	list_display = ('ip_segment','client','hub','edge_name')
	def save_model(self, request, obj, form, change):
		#definir
		obj.edge_name = obj.client.name
		portgroup_id = getPortgroupId(obj.hub.uplink_pg)
		jinja_vars = {  "datacenterMoid" : 'datacenter-2',
						"name" : 'Edge-Test-Django',
						"description" : "",
						"appliances" : {    "applianceSize" : 'xlarge',
																"appliance" : {"resourcePoolId" : obj.hub.resource_pool_id,
																			 "datastoreId" : obj.hub.datastore_id
																			}},
				"vnics" : [{"index" : "0",
										"name" : "uplink",
										"type" : "Uplink",
										"portgroupId" : portgroup_id,
										"primaryAddress" : "192.168.0.1",
										"subnetMask" : "255.255.255.0",
										"mtu" : "1500",
										"isConnected" : "true"
									 }],
				"cliSettings" : {"userName" : "admin",
												 "password" : "T3stC@s3NSx!",
												 "remoteAccess" : "true"}
				}

		# result = createNsxEdge(jinja_vars)

		super(PrivateIrsAdmin, self).save_model(request, obj, form, change)

class ClientAdmin (admin.ModelAdmin):
	list_display = ['name']
	def save_model(self, request, obj, form, change):
		super(ClientAdmin, self).save_model(request, obj, form, change)

class PortgroupAdmin(admin.ModelAdmin):
	list_display = ['name','vlan_tag', 'hub']

admin.site.register(Hub)
admin.site.register(Portgroup,PortgroupAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(PrivateIrsService,PrivateIrsAdmin)
admin.site.register(PublicIrsService)
