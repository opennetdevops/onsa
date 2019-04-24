from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View
from jeangrey.models import *
from jeangrey.utils import *

import jeangrey.models as models
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class CustomerLocationAccessPortsView(View):

    def get(self, request, client_id, customer_location_id):
    
        try:
            s = Service.objects.get(client_id=client_id, customer_location_id=customer_location_id) 
            data = s.fields()   
            response = []
            for s in data:
                access_port = get_access_port(s['access_port_id'])
                access_node = get_access_node(s['access_node_id'])
                response.append({'access_port': access_port['port'], 'access_node': access_node['name']})   
            return JsonResponse(list(response), safe=False) 

        except Service.DoesNotExist as e:
            logging.error(e)
            return JsonResponse({"msg": str(e)}, safe=False, status=ERR_NOT_FOUND)