from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin


from rest_framework_jwt.views import obtain_jwt_token

from django.views.decorators.http import require_http_methods

from .views import service
import os

urlpatterns = [ 
    path('/api/services', require_http_methods(["POST","GET"])(service.ServiceView.as_view())),
    path('/api/services/<str:service_id>', require_http_methods(["GET","PUT","DELETE"])(service.ServiceView.as_view())),    
    path('/api/services/<str:service_id>/process', require_http_methods(["POST"])(service.ProcessView.as_view())),
 ]