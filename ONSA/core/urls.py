from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.http import require_http_methods

from .views import service, client, pending_services, client_nodes, cpe_ports


urlpatterns = [ 
    url(r'^select2/', include('django_select2.urls')),
    path('/api/login', obtain_jwt_token),
    path('/api/services', require_http_methods(["GET","POST"])(service.ServiceView.as_view())),
    path('/api/services/<str:service_id>', require_http_methods(["GET","PUT"])(service.ServiceView.as_view())),
    path('/api/clients', require_http_methods(["GET","POST"])(client.ClientView.as_view())),
    path('/api/clients/<int:client_id>', require_http_methods(["GET"])(client.ClientView.as_view())),
    path('/api/clientnodes', require_http_methods(["GET","POST"])(client_nodes.ClientNodesView.as_view())),
    path('/api/clientnodes/<int:client_node_id>', require_http_methods(["GET","POST"])(client_nodes.ClientNodesView.as_view())),
    path('/api/cpeports', require_http_methods(["GET","POST"])(cpe_ports.CpePortsView.as_view())),
    path('/api/pending_services', require_http_methods(["GET","POST"])(pending_services.PendingServiceView.as_view())),
    path('/api/pending_services/<str:service_id>', require_http_methods(["GET","PUT"])(pending_services.PendingServiceView.as_view())),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
