from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from .views import devices
from .views import test_view
from .views.locations import RouterNode, AccessNode



urlpatterns = [ 
    path('api/login', obtain_jwt_token),
    path('api/devices', devices.devices),
    path('api/test', test_view.test),
    path('api/v1/location/<str:location_name>/routernode', RouterNode.as_view()),
    path('api/v1/location/<str:location_name>/accessnode/<int:access_id>', AccessNode.as_view())
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
