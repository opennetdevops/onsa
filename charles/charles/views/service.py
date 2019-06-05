from django.conf import settings
from django.http import JsonResponse
from django.views import View
from charles.models import Service
from charles.utils import *
from pprint import pprint

import requests
import json
import logging

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

        try:
            if not self._existing_service(data['service_id']):
                # Create Service instance on charles
                Service.objects.create(
                    service_id=data['service_id'], target_state=data['target_state'], deployment_mode=data['deployment_mode'])
            else:
                charles_service = Service.objects.get(
                    service_id=data['service_id'])
                charles_service.reprocess(
                    target_state=data['target_state'], deployment_mode=data['deployment_mode'])

            # Update charles service with JeanGrey's data
            service = get_service(data['service_id'])
            my_charles_service = Service.objects.filter(
                service_id=data['service_id']).values()[0]
            my_charles_service.update(service)

            # Run FSM over charles service
            service_state = Fsm.run(my_charles_service)

        except BaseException as e:
            return e.handle()

        msg = {"message": "Service requested."}
        return JsonResponse(msg, status=HTTP_201_CREATED)

    def put(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))

        # if data['service_state'] == 0:
        #   service = Service.objects.get(service_id=service_id)
        #   service.service_state = NextStateE2e[service.service_state].value
        #   service.save()

        #   update_jeangrey_service(service_id, {'service_state': service.service_state})

        #   if service.service_state != service.target_state:
        #       service = get_service(service_id)
        #       client = get_client(service['client_id'])

        #       generate_request = getattr(ServiceTypes[service['service_type']].value, "generate_" + service['service_type'] + "_request")
        #       request, service_state = generate_request(client, service, code="cpe")
        #       pprint(request)

        # # Rollback all reservations if error
        # # if service[0].service_state == "ERROR":
        # #     rollback_service(str(service_id))

        response = {"message": "Service state updated"}

        return JsonResponse(response, safe=False)

    def _existing_service(self, service_id):
        return Service.objects.filter(service_id=service_id).count() is not 0

    def delete(self, request, service_id):
        logging.debug(f'processing DELETE of service id: {service_id}')
        my_service = Service.objects.filter(service_id=service_id).values()[0]
        my_service_obj = Service.objects.get(service_id=service_id)
        service = get_service(service_id)

        if service['service_state'] != INITIAL_SERVICE_STATE:

            if service['service_state'] == DELETEINPROGRESS_SERVICE_STATE:
                logging.debug(f'already marked for deletion')
                response = {"msg": "Service already marked for deletion"}
            else:

                data = {'service_state': TOBEDELETED_SERVICE_STATE}
                update_jeangrey_service(my_service['service_id'], data)
                my_service_obj.service_state = TOBEDELETED_SERVICE_STATE
                my_service_obj.target_state = DELETED_SERVICE_STATE
                my_service_obj.save()

                my_service = Service.objects.filter(
                    service_id=service_id).values()[0]
                my_service.update(service)
                my_service['service_state'] = TOBEDELETED_SERVICE_STATE

                try:
                    service_state = Fsm.run(my_service)
                except BaseException as e:
                    service_state = DELETEERROR_SERVICE_STATE
                    data = {'service_state': service_state}
                    update_jeangrey_service(my_service['service_id'], data)
                    my_service_obj.service_state = service_state
                    my_service_obj.save()
                    response = {"msg": "Error deleting service"}
                    return JsonResponse(response, status=ERR_COULDNT_DELETESERVICE)

                response = {"msg": "Service marked for deletion"}
        else:
            my_service.delete()
            response = {"msg": "Service deleted successfully"}
        
        return JsonResponse(response, status=HTTP_204_NO_CONTENT)



class ProcessView(View):

    def post(self, request, service_id):
        data = json.loads(request.body.decode(encoding='UTF-8'))
        logging.debug(str("processing service id:" + service_id +
                          " with code: " + data['service_state']))
        my_service = Service.objects.filter(service_id=service_id).values()[0]
        my_service_obj = Service.objects.get(service_id=service_id)
        service = get_service(service_id)
        my_service.update(service)
        logging.debug("Updated service: ")
        logging.debug(my_service)

        if data['service_state'] != "ERROR":

            service_state = next_state(
                my_service['service_state'], my_service['target_state'])

            logging.debug(
                str("Going to update JG service to: " + service_state))
            data = {'service_state': service_state}
            update_jeangrey_service(my_service['service_id'], data)
            logging.debug("JG updated, updating charles...")

            my_service_obj.service_state = service_state
            my_service_obj.save()
            logging.debug("Charles updated")

            my_service = Service.objects.filter(
                service_id=service_id).values()[0]
            my_service.update(service)
            my_service['service_state'] = service_state

            if service_state != my_service['target_state']:
                logging.debug(
                    "current state different than target_state, running FSM with service:")
                logging.debug(str(my_service))

                try:
                    service_state = Fsm.run(my_service)

                except BaseException as e:
                    service_state = "ERROR"
                    data = {'service_state': service_state}
                    update_jeangrey_service(my_service['service_id'], data)
                    my_service_obj.service_state = service_state
                    my_service_obj.save()
                    return e.handle()

                print("second: ", service_state)
                print(my_service)
            response = {"message": "Service state updated"}

        else:
            service_state = "ERROR"
            response = {"message": "Service update failed"}

        data = {'service_state': service_state}
        update_jeangrey_service(my_service['service_id'], data)
        my_service_obj.service_state = service_state
        my_service_obj.save()
        return JsonResponse(response, safe=False)
