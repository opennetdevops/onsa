from django.conf import settings
from django.http import JsonResponse
from django.views import View
from charles.models import Service
from charles.utils.fsm import Fsm
from charles.utils.utils import *
from pprint import pprint

import logging
import requests
import json


class ServiceView(View):

    def get(self, request, service_id=None):

        if service_id is None:
            services = Service.objects.all().values()
            return JsonResponse(list(services), safe=False)
        else:
            service = Service.objects.filter(service_id=service_id).values()[0]
            return JsonResponse(service, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        # Retry support
        if not self._existing_service(data['service_id']):
            charles_service = Service.objects.create(service_id=data['service_id'], target_state=data['target_state'], deployment_mode=data['deployment_mode'])
        else:
            charles_service = Service.objects.get(service_id=data['service_id'])
            charles_service.target_state = data['target_state']
            charles_service.deployment_mode = data['deployment_mode']


        service = get_service(data['service_id'])
        charles_service_state = service['service_state']

        #for persistence
        charles_service.save()

        my_charles_service = Service.objects.filter(service_id=data['service_id']).values()[0]
        my_charles_service.update(service)

        pprint(my_charles_service)

        try:
            service_state = Fsm.run(my_charles_service)
        except ClientPortException as err:
            logging.error(err)
            return JsonResponse(status=ERR_NO_CLIENTPORTS)
        except CustomerLocationException as err:
            logging.error(err)
            return JsonResponse(status=ERR_NO_CUSTOMERLOCATIONS)
        except ClientNodeException as err:
            logging.error(err)
            return JsonResponse(status=ERR_NO_CLIENTNODE)
        

        if service_state is not None:
            charles_service.service_state = service_state
            response = { "message": "Service requested." }
        else:
            charles_service.service_state = "error"
            response = { "message": "Service request failed." }

        charles_service.save()
        update_service(data['service_id'], {'service_state': service_state} )

        return JsonResponse(response, status=HTTP_201_CREATED)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        # if data['service_state'] == 0:
        #   service = Service.objects.get(service_id=service_id)
        #   service.service_state = NextStateE2e[service.service_state].value
        #   service.save()

        #   update_service(service_id, {'service_state': service.service_state})

        #   if service.service_state != service.target_state:
        #       service = get_service(service_id)
        #       client = get_client(service['client_id'])

        #       generate_request = getattr(ServiceTypes[service['service_type']].value, "generate_" + service['service_type'] + "_request")
        #       request, service_state = generate_request(client, service, code="cpe")
        #       pprint(request)

        # # Rollback all reservations if error
        # # if service[0].service_state == "ERROR":
        # #     rollback_service(str(service_id))

        response = { "message": "Service state updated" }

        return JsonResponse(response, safe=False)


    def delete(self, request, service_id):
        svc = Service.objects.filter(service_id=service_id)
        svc.delete()
        data = {"Message" : "Service deleted successfully"}
        return JsonResponse(data)


    def _existing_service(self, service_id):
        return Service.objects.filter(service_id=service_id).count() is not 0



class ProcessView(View):

    def post(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        my_service = Service.objects.filter(service_id=service_id).values()[0]
        my_service_obj = Service.objects.get(service_id=service_id)
        service = get_service(service_id)
        my_service.update(service)

        if data['service_state'] != "ERROR":
            service_state = Fsm.to_next_state(my_service)
            data = {'service_state': service_state}
            update_service(my_service['service_id'], data)
            my_service_obj.service_state = service_state
            my_service_obj.save()
            my_service = Service.objects.filter(service_id=service_id).values()[0]
            my_service.update(service)
            my_service['service_state'] = service_state
            

            if service_state != my_service['target_state']:
                service_state = Fsm.run(my_service)
                print("second: ", service_state)
                print(my_service)
            response = { "message": "Service stated updated" }

        else:
            service_state = "error"
            response = { "message": "Service update failed" }

        data = {'service_state': service_state}
        update_service(my_service['service_id'], data)
        my_service_obj.service_state = service_state
        my_service_obj.save()
        return JsonResponse(response, safe=False)

