from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from .views import service

urlpatterns = [ 
    path('/api/services', require_http_methods(["PUT","POST","GET"])(service.ServiceView.as_view()))    
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)