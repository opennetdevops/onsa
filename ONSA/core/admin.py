from django.contrib import admin
from pprint import pprint
from .models import *
from .forms import *
from ipaddress import *


def service_type(self):
    return self.service.service_type

def service_bandwidth(self):
    return self.service.bandwidth

def service_vrf(self):
    return self.service.vrf

def service_id(self):
    return self.service.pk

def client_name(self):
    return self.client.name

def client_node_sn(self):
    return self.cpe_port.cpe.serial_number

def client_node_port(self):
    return self.cpe_port.name


class ServiceCpeRelationsAdmin(admin.ModelAdmin):
    form = ServiceCpeRelationForm

    list_display = (client_name, service_id, service_type, client_node_sn, client_node_port, service_bandwidth)
    # list_filter = ('client')
    actions = ['delete_selected']

    # exclude = ('client', 'client_node_sn', 'client_node_port', 'bandwidth', 'prefix' , service_vrf)



    def save_model(self, request, obj, form, change):
        obj.client = obj.service.client
        obj.client_name = obj.service.client.name
        obj.bandwidth = obj.service.bandwidth
        obj.prefix = obj.service.prefix
        obj.vrf = obj.service.vrf
        obj.service_state = obj.service.service_state
        obj.product_identifier = obj.service.product_identifier
        obj.client_node_sn = obj.cpe_port.cpe.serial_number
        obj.client_node_port = obj.cpe_port.name
        obj.service_type = obj.service.service_type

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

    list_display = ('client', 'product_identifier', 'bandwidth')
    actions = ['delete_selected']

    exclude = ['vrf']

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

