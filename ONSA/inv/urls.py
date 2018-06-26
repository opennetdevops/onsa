from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from . import views


# admin.autodiscover()

urlpatterns = [ 
    url(r'^api/login', obtain_jwt_token)
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
