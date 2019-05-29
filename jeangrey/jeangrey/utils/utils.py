from django.conf import settings
from jeangrey.exceptions import *
from jeangrey.constants import *

import json
import requests
import logging
import coloredlogs
import os
import sys

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_inventory_authentication_token():
    url = "authenticate"
    rheaders = {'Content-Type': 'application/json'}
    data = {"email":os.getenv('INVENTORY_USER'), "password":os.getenv('INVENTORY_PASSWORD')}
    response = requests.post(os.getenv('INVENTORY_URL') + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    # logging.debug(response.text)
    return json.loads(response.text)['auth_token']


def get_access_node(access_node_id):
    url = settings.INVENTORY_URL + "access_nodes/"+ str(access_node_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise AccessNodeException("Invalid Access Node.", status_code=r.status_code)

def get_access_port(access_port_id):
    url = settings.INVENTORY_URL + "access_ports/"+ str(access_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise AccessPortException("Invalid Access Port.", status_code=r.status_code)

def get_service_vrfs(vrf_id):
    url = settings.JEAN_GREY_URL + "services?vrf_id="  + str(vrf_id)
    rheaders = {'Content-Type': 'application/json'}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise VrfException("Could not resolve request.", status_code=r.status_code)

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


#TODO SE USA
def get_router_node(location_id):
    url = settings.INVENTORY_URL + "locations/" + str(location_id) + "/router_nodes"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.status_code != HTTP_200_OK:
        raise LocationException("Invalid location.", status_code=r.status_code)
    else:
        
        if len(r.json()):
           return r.json()[0]
        return r.json()	
    
def get_router_nodes(location_id):
    url = settings.INVENTORY_URL + "locations/" + str(location_id) + "/router_nodes"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.status_code != HTTP_200_OK:
        raise LocationException("Invalid location.", status_code=r.status_code)
    else:
        return r.json()


def get_free_access_port(location_id):
    url = settings.INVENTORY_URL + "locations/"+ str(location_id) + "/access_ports?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    print(r.json())
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()[0]
    elif not r.json():
        raise LocationException("Not available AccessPort", status_code=ERR_NO_ACCESSPORTS)
    else:
        raise LocationException("Invalid location.", status_code=r.status_code)

def get_location_id(location_name):
    url = settings.INVENTORY_URL + "locations?name=" + location_name
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()[0]['id']
    else:
        raise LocationException("Could not resolve request", status_code=r.status_code)

def use_access_port(access_port_id):
    url = settings.INVENTORY_URL + "access_ports/" + access_port_id
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":True}
    r = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise AccessPortException("Invalid access port.", status_code=r.status_code)

def get_client_vrfs(client_name):
    url = settings.INVENTORY_URL + "vrfs?client="+client_name
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise VrfException("Could not resolve request.", status_code=r.status_code)


def get_free_vrf():
    url = settings.INVENTORY_URL + "vrfs?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()[0]
    else:
        raise VrfException("Could not resolve request.", status_code=r.status_code)


def use_vrf(vrf_id, vrf_name, client_name):
    url = settings.INVENTORY_URL + "vrfs/" + vrf_id
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":True, "name": vrf_name, "client": client_name}
    r = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise VrfException("Invalid VRF Id.", status_code=r.status_code)

def get_free_vlan(access_node_id):
    url = settings.INVENTORY_URL + "access_nodes/"+ str(access_node_id) + "/vlans?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    logging.debug(r.json())
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()[0]
    elif not r.json():
        raise AccessNodeException("Not available VLANs", status_code=ERR_NO_VLANS)
    else:
        raise AccessNodeException("Invalid access node.", status_code=r.status_code)


def use_vlan(access_node_id, vlan_id):
    url = settings.INVENTORY_URL + "access_nodes/" + str(access_node_id) + "/vlans"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = { 'vlan_id': vlan_id }
    r = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_201_CREATED:
        return r.json()
    else:
        raise AccessNodeException("Invalid access node.", status_code=r.status_code)

def get_vrf(vrf_name):
    url = settings.INVENTORY_URL + "vrfs?name="+ vrf_name
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise VrfException("Invalid VRF Id.", status_code=r.status_code)

def release_access_port(access_port_id):
    url = settings.INVENTORY_URL + "access_ports/" + access_port_id
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":False}
    r = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise AccessPortException("Invalid access port.", status_code=r.status_code)


def release_vlan(access_node_id, vlan_id):
    url = settings.INVENTORY_URL + "access_nodes/" + str(access_node_id) + "/vlans"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = { 'vlan_id': vlan_id }
    r = requests.delete(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    return r.json()

        
def release_resources(allocated_resources):
    for elem in allocated_resources:
        release_func = getattr(sys.modules[__name__], "release_" + elem)
        release_func(allocated_resources[elem])