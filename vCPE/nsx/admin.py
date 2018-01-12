from django.contrib import admin
from pprint import pprint
from .lib.utils.nsx.edge import *
from .lib.utils.vcenter.GetPortgroups import *
from .models import *
from .forms import *






class PublicIrsAdmin (admin.ModelAdmin):
	#exclude = ('edge_name', 'portgroup')
	list_display = ('ip_segment','client','edge_name')
	list_filter = ('client', 'edge_name')

	form = IrsServiceForm





class PrivateIrsAdmin(admin.ModelAdmin):
	form = IrsServiceForm

	list_display = ('ip_segment','client','edge_name','hub')
	list_filter = ('client', 'edge_name')

	exclude = ('edge_name', 'portgroup')

	def hub(self, obj):
		return obj.portgroup.hub


	def save_model(self, request, obj, form, change):

		#Create NSX Edge

		obj.edge_name = obj.client.name
		print("Hub Name: ",form.cleaned_data['hub'].name)
		print("SCO Name: ",form.cleaned_data['sco'].name)
		pg = Portgroup.getFreePortgroupAtHub(form.cleaned_data['hub'].name)
		print("Portgroup Name: ", pg.name)
		obj.portgroup = pg

		
		#portgroup_id = getPortgroupId(obj.hub.uplink_pg)
		# jinja_vars = {  "datacenterMoid" : 'datacenter-2',
		# 				"name" : 'Edge-Test-Django',
		# 				"description" : "",
		# 				"appliances" : {    "applianceSize" : 'xlarge',
		# 														"appliance" : {"resourcePoolId" : obj.hub.resource_pool_id,
		# 																	 "datastoreId" : obj.hub.datastore_id
		# 																	}},
		# 		"vnics" : [{"index" : "0",
		# 								"name" : "uplink",
		# 								"type" : "Uplink",
		# 								"portgroupId" : portgroup_id,
		# 								"primaryAddress" : "192.168.0.1",
		# 								"subnetMask" : "255.255.255.0",
		# 								"mtu" : "1500",
		# 								"isConnected" : "true"
		# 							 }],
		# 		"cliSettings" : {"userName" : "admin",
		# 										 "password" : "T3stC@s3NSx!",
		# 										 "remoteAccess" : "true"}
		# 		}

		# result = createNsxEdge(jinja_vars)
		# print(form.cleaned_data)

		super(PrivateIrsAdmin, self).save_model(request, obj, form, change)

class ClientAdmin (admin.ModelAdmin):
	list_display = ['name']

	def save_model(self, request, obj, form, change):
		super(ClientAdmin, self).save_model(request, obj, form, change)

class PortgroupAdmin(admin.ModelAdmin):
	list_display = ['name','vlan_tag', 'hub']






admin.site.register(Hub)
admin.site.register(Sco)
admin.site.register(ScoPort)
admin.site.register(IpWan)
admin.site.register(IpPublicSegment)

admin.site.register(Portgroup,PortgroupAdmin)
admin.site.register(Client,ClientAdmin)

admin.site.register(PrivateIrsService,PrivateIrsAdmin)
admin.site.register(PublicIrsService,PublicIrsAdmin)