from django.contrib import admin
from jeangrey.models import Client, CustomerLocation, CpelessIrs, CpeMpls, CpeIrs, Vpls, VcpeIrs, CpelessMpls, Tip, Legacy

# Register your models here.
admin.site.register(CpelessIrs)
admin.site.register(CpeMpls)
admin.site.register(CpeIrs)
admin.site.register(Vpls)
admin.site.register(VcpeIrs)
admin.site.register(CpelessMpls)
admin.site.register(Tip)
admin.site.register(Client)
admin.site.register(Legacy)
admin.site.register(CustomerLocation)