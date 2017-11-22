from django.contrib import admin
from .lib.utils.nsx.edge import *
from .models import Hub, Portgroup, Client, PrivateIrsService, PublicIrsService

class PrivateIrsAdmin (admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
	  super(PrivateIrsAdmin, self).save_model(request, obj, form, change)

class ClientAdmin (admin.ModelAdmin):
	list_display = ['name']
	def save_model(self, request, obj, form, change):
		super(ClientAdmin, self).save_model(request, obj, form, change)

admin.site.register(Hub)
admin.site.register(Portgroup)
admin.site.register(Client,ClientAdmin)
admin.site.register(PrivateIrsService,PrivateIrsAdmin)
admin.site.register(PublicIrsService)
