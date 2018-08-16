from django.contrib import admin
from pprint import pprint
from .models import *
from .forms import *
from ipaddress import *


class ServiceCpeRelationsAdmin(admin.ModelAdmin):
    form = ServiceCpeRelationForm

    list_display = ('cpe_port', 'service', 'bandwidth', 'prefix' , 'vrf')
    # list_filter = ('client')
    actions = ['delete_selected']

    exclude = ('client', 'client_node_sn', 'client_node_port')



    def save_model(self, request, obj, form, change):
        obj.client = obj.service.client.name
        obj.bandwidth = form.cleaned_data['bandwidth']
        obj.public_network = form.cleaned_data['public_network']
        obj.prefix = form.cleaned_data['prefix']
        obj.vrf = form.cleaned_data['vrf']



        super(ServiceCpeRelationsAdmin, self).save_model(request, obj, form, change)
  
        
    def delete_model(self, request, obj):
        obj.delete()


    def delete_selected(self, request, obj):

        for o in obj.all():
            # delete object
            o.delete()




class ClientAdmin (admin.ModelAdmin):
    list_display = ['name']

    def save_model(self, request, obj, form, change):
        super(ClientAdmin, self).save_model(request, obj, form, change)



class ServiceAdmin(admin.ModelAdmin):
    # form = IrsServiceForm

    list_display = ('client', 'service_id', 'product_identifier', 'bandwidth', 'public_network', 'prefix' , 'vrf')
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        # client = Client.objects.get(name=form.cleaned_data['client'])
        # service_id = form.cleaned_data['service_id']
        # product_identifier = form.cleaned_data['product_identifier']
        # bandwidth = form.cleaned_data['bandwidth']
        # public_network = form.cleaned_data['public_network']
        # prefix = form.cleaned_data['prefix']
        # vrf = form.cleaned_data['vrf']

        # a = ServiceCpeRelations.create()

        super(ServiceAdmin, self).save_model(request, obj, form, change)


# Register

admin.site.register(Client,ClientAdmin)
admin.site.register(Cpe)
admin.site.register(CpePort)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCpeRelations, ServiceCpeRelationsAdmin)

