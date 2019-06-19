from celery import shared_task
from django.http import HttpResponse, JsonResponse
from worker.models import Service, Task
from worker.constants import *
import logging
import json


@shared_task
def process_service(request):
    logging.debug("My req: " + request)
    data = json.loads(request)
    logging.debug("my data")
    logging.debug(data)

    """
    Create service based on:

    service_id: Service identifier

    service_type: Can be any type of service, such as
    VCPE-IRS, VCPE-MPLS, CPE-IRS, CPE-MPLS, CPELESS-IRS, CPELESS-MPLS

    service_state: Status of the actual service after being requested

    """

    if Service.objects.filter(service_id=data['service_id']).count() is 0:
        service = Service(client_name=data['client'],
                          service_id=data['service_id'],
                          service_type=data['service_type'],
                          service_state="IN_PROGRESS",
                          parameters=data['parameters'])
        service.save()
    else:
        service = Service.objects.filter(service_id=data['service_id'])
        service.update(parameters=data['parameters'])
        service = service[0]

    """
    Creates all of the tasks associated with
    the service requested.
    """
    for device in data['devices']:
        task = Task(service=service,
                    op_type=data['op_type'],
                    device=device,
                    task_state=INITIAL_TASK_STATE)
        task.save()

    service.deploy()
    return

# TODO
@shared_task
def re_process_service(request):
    logging.debug("My req: " + request)
    data = json.loads(request)
    logging.debug("my data")
    logging.debug(data)

    # look for tasks referred to that service id
    # re-run tasks
    # update service

    return
