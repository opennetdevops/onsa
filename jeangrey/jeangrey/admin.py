from django.contrib import admin
from jeangrey.models.models import Client, CustomerLocation, Service

# Register your models here.
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(CustomerLocation)