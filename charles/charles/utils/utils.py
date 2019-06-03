from charles.constants import *
from charles.exceptions import *
from charles.models import Service
from charles.utils.inventory_utils import *
from charles.utils.ipam_utils import *

import requests
import json
import os
import logging
import coloredlogs
from celery import Celery
import kombu



def configure_service(config):
    #TODO User pass and server from local/production
    
    #just triggered to test connection to RMQ, currently there is no support from celery worker
    try:
        a = kombu.Connection('amqp://myuser:mypassword@10.120.78.58/myvhost',connect_timeout=3)
        a.connect()
        a.release()

        app = Celery('worker', broker='amqp://myuser:mypassword@10.120.78.58/myvhost', broker_pool_limit=None)
        promise = app.send_task('worker.tasks.process_service', args=[json.dumps(config)], ignore_result=True )
        logging.info("Sending message to queue")
    except BaseException:
        raise MessagingException("Unable to push message to queue")






def update_jeangrey_service(service_id, data):
    url = os.getenv('JEAN_GREY_URL') + "services/" + str(service_id)
    rheaders = {'Content-Type': 'application/json'}

    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise ServiceException("Unable to update service")


def rollback_service(service_id):
    #TODO: NOT IMPLEMENTED
    #TODO: NOT IMPLEMENTED
    #TODO: NOT IMPLEMENTED
    pass


def update_core_service_status(service_id, data):
    rheaders = {'Content-Type': 'application/json'}
    url = os.getenv('CORE_URL') +"services/" + str(service_id)
    response = requests.put(url, data = json.dumps(data), headers=rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Unable to update core service")


def get_service(service_id):
    url = os.getenv('JEAN_GREY_URL') + "services/" + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Invalid Service")

def get_access_port_services(access_port_id):
    url = os.getenv('JEAN_GREY_URL') + "services?access_port_id=" + str(access_port_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Invalid Service")

def get_services():
    url = os.getenv('JEAN_GREY_URL') + "services"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Unable to retrieve services")

def get_charles_services():
    url = os.getenv('CHARLES_URL') + "services"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Unable to retrieve services")

def get_client(client_id):
    url = os.getenv('JEAN_GREY_URL') + "clients/"  + str(client_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientException("Invalid Client")

def delete_client(client_id):
    url = os.getenv('JEAN_GREY_URL') + "clients/"  + str(client_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ClientException("Invalid Client")


def delete_service(service_id):
    url = os.getenv('CORE_URL') + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Invalid Service")


def delete_charles_service(service_id):
    url = os.getenv('CHARLES_URL') + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete charles Service")

def delete_jeangrey_service(service_id):
    url = os.getenv('JEAN_GREY_URL') + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete Jean Grey Service")


def delete_customer_location(client_id, customer_location_id):
    url = os.getenv('JEAN_GREY_URL') + "clients/"  + str(client_id) + "/customerlocations/" + str(customer_location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise CustomerLocationException("Unable to delete Customer Location")

def get_client_by_name(client_name):
    url = os.getenv('JEAN_GREY_URL') + "clients?name="  + str(client_name)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientException("Unable to retrieve Client")

def get_clients():
    url = os.getenv('JEAN_GREY_URL') + "clients"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientException("Unable to retrieve clients")




def get_customer_location(client_id, customer_location_id):
    url = os.getenv('JEAN_GREY_URL') + "clients/"  + str(client_id) +"/customerlocations/" + str(customer_location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise CustomerLocationException("Invalid customer location")

def get_customer_locations(client_id):
    url = os.getenv('JEAN_GREY_URL') + "clients/"  + str(client_id) +"/customerlocations"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise CustomerLocationException("No available customer locations")

def create_customer_location(client_id):
    url = os.getenv('JEAN_GREY_URL') + "clients/"  + str(client_id) +"/customerlocations"
    rheaders = {'Content-Type': 'application/json'}
    data = {"address":"my_address","description":"some_description"}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise CustomerLocationException("Unable to create Customer Location")
    

def create_client(client_name):
    url = os.getenv('JEAN_GREY_URL') + "clients" 
    rheaders = {'Content-Type': 'application/json'}
    data = {"name":client_name}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ClientException("Unable to create Client")

def login_core():
    url = os.getenv('CORE_URL') +"login" 
    rheaders = {'Content-Type': 'application/json'}
    data = {"username":"fc__netauto@lab.fibercorp.com.ar", "password":"F1b3rc0rp!"}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response['token']
    else:
        raise ServiceException("Unable to login to core service")

def create_core_service(data, token):
    url = os.getenv('CORE_URL') +"services" 
    rheaders = {'Content-Type': 'application/json', 'Authorization': "Bearer " + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Unable to create service through core API")


def fetch_cpe_port_id(client_node_sn, client_name, customer_location):
    client_node = get_client_node(client_node_sn)

    """
    Update Inventory with CPE data if needed
    """
    if client_node['client'] is None:
        cpe_data = { 'client': client_name, 'customer_location': customer_location['address'] }
        update_cpe(client_node_sn, cpe_data)

    """
    Get free CPE port from Inventory and
    mark it as a used port.
    """
    cpe_port = get_free_cpe_port(client_node_sn)
    if cpe_port == [] or cpe_port is None:
        raise ClientPortException("No free client port on CPE")
    else:
        cpe_port_id = cpe_port['id']
        #Assign CPE Port (mark as used)
        use_client_node_port(client_node_sn, cpe_port_id)
        return cpe_port_id


def push_service_to_orchestrator(service_id, deployment_mode, target_state):
    url = os.getenv('CHARLES_URL') + "services"
    rheaders = { 'Content-Type': 'application/json' }   
    data = { "service_id": service_id, "deployment_mode": deployment_mode, "target_state": target_state }   
    response = requests.post(url, data = json.dumps(data), headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to push service to orchestrator")


def update_charles_service_state(service_id, state):
    url = os.getenv('CHARLES_URL') + "services/" + str(service_id) + "/process"
    rheaders = { 'Content-Type': 'application/json' }   
    data = { "service_state": state }   
    response = requests.post(url, data = json.dumps(data), headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Unable to update charles service")


def get_service_vrfs(vrf_id):
    url = os.getenv('JEAN_GREY_URL') + "services?vrf_id="  + str(vrf_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to retrieve Vrf")






def assign_autonomous_system(vrf_id):    
    list_vrfs = get_service_vrfs(vrf_id)

    if list_vrfs is None:
        return 65000

    list_as = list(map(lambda x: x['autonomous_system'], list_vrfs))

    if (len(list_as) == 1) and (list_as[0] is 0):
        return 65000

    ordered_list_as = sorted(list_as, key=lambda k: k)
    last_as = int( ordered_list_as[-1] )

    if last_as <= 65500:
        return (last_as + 1)
    else:
        while(1):
            proposed_as = 65000
            if proposed_as > 65500:
                #TODO throw exception
                return -1

            if Service.objects.filter(vrf_name=vrf_name, autonomous_system=proposed_as).values().count():
                proposed_as+=1
            else:
                return proposed_as



def update_charles_service(service, state):
    charles_service = Service.objects.get(service_id=service['service_id'])
    charles_service.last_state = charles_service.service_state
    service['last_state'] = charles_service.service_state
    charles_service.service_state = state
    service['service_state'] = state
    charles_service.save()
    return service


