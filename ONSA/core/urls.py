"""vCPE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from . import views


# admin.autodiscover()

urlpatterns = [ 
    url(r'^api/login', obtain_jwt_token),
    url(r'^api/scos/', views.scos),
    url(r'^api/scoports/', views.scoports),
    url(r'^api/privateirsservices/', views.privateirsservices),
    url(r'^api/portgroups/', views.portgroups),
    url(r'^api/logicalunits/', views.logicalunits),
    url(r'^api/ipwans/', views.ipwans),
    url(r'^api/ippublicsegments/', views.ippublicsegments),
    url(r'^api/publicirsservices/', views.publicirsservices),
    url(r'^api/hubs/', views.hubs),
    url(r'^api/clients/', views.clients),
    url(r'^api/transportzones/', views.transportzones),
    url(r'^api/datacenter/', views.datacenter),
    url(r'^api/datacenters/', views.datacenters),
    url(r'^api/logicalswitch/', views.logicalswitch),
    url(r'^api/logicalswitches/', views.logicalswitches),
    url(r'^api/edge/', views.edge),
    url(r'^api/edges/', views.edges),
    url(r'^select2/', include('django_select2.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
