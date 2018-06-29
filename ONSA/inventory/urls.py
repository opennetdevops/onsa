from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from . import views



urlpatterns = [ 
    url(r'^api/login', obtain_jwt_token),
    url(r'^api/devices', views.devices)
#     url(r'^api/accessPorts/', views.scoports),
#     url(r'^api/portgroups/', views.portgroups),
#     url(r'^api/logicalunits/<pk[0-9]+>', views.logicalunits),
#     url(r'^api/locations', views.locations),
#     url(r'^api/edge/', views.edge),
#     url(r'^api/edges/', views.edges)
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
