from django.contrib import admin
from .models import Hub, Portgroup, Client, PrivateIrsService, PublicIrsService

# Register your models here.

admin.site.register(Hub)
admin.site.register(Portgroup)
admin.site.register(Client)
admin.site.register(PrivateIrsService)
admin.site.register(PublicIrsService)