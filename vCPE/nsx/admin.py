from django.contrib import admin
from .models import Hub, Portgroup, Client, PrivateIrsService, PublicIrsService



class ClientAdmin (admin.ModelAdmin):
    def has_add_permission(self, request):
        return False





# Register your models here.
admin.site.register(Hub)
admin.site.register(Portgroup)
admin.site.register(Client, ClientAdmin)
admin.site.register(PrivateIrsService)
admin.site.register(PublicIrsService)


