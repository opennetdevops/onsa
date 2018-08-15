from django.contrib import admin

from pprint import pprint
from .models import *
# from .forms import *
from ipaddress import *

# class NsxPublicIrsAdmin(admin.ModelAdmin):
#     # form = IrsServiceForm
#     # list_display = ('public_network','client','edge_name','hub', 'sco', 'sco_port', 'product_identifier')
#     # list_filter = ('client', 'edge_name')
#     actions = ['delete_selected']

#     exclude = ('edge_name', 'portgroup', 'public_network')

#     def save_model(self, request, obj, form, change):

#         super(NsxPublicIrsAdmin, self).save_model(request, obj, form, change)


# Register
admin.site.register(VlanTag)
admin.site.register(AccessPort)
#admin.site.register(OpticalNode)
admin.site.register(ClientNode)
admin.site.register(RouterNode)
admin.site.register(AccessNode)

admin.site.register(Portgroup)
admin.site.register(Location)
admin.site.register(VirtualVmwPod)
admin.site.register(NsxEdge)
admin.site.register(LogicalUnit)
admin.site.register(VlantagAccessports)
# admin.site.register(Vrf)