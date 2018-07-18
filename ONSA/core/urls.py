from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.http import require_http_methods

from .views import service


# admin.autodiscover()

urlpatterns = [ 
    path('/api/login', obtain_jwt_token),
    path('/api/services', require_http_methods(["GET","POST"])(service.ServiceView.as_view())),
    path('/api/services/<int:service_id>', require_http_methods(["GET","PUT"])(service.ServiceView.as_view())),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
