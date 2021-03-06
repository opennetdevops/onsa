from charles.constants import *
from charles.exceptions import *
from charles.models import Service
from django.conf import settings


import requests
import json
import os
import logging
import coloredlogs


def get_inventory_authentication_token():
    url = "authenticate"
    rheaders = {'Content-Type': 'application/json'}
    data = {"email":os.getenv('INVENTORY_USER'), "password":os.getenv('INVENTORY_PASSWORD')}
    response = requests.post(os.getenv('INVENTORY_URL') + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    # logging.debug(response.text)
    return json.loads(response.text)['auth_token']


### CREATE METHODS 
def create_access_node(data):
    url = os.getenv('INVENTORY_URL') + "access_nodes"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")

def create_router_node(data):
    url = os.getenv('INVENTORY_URL') + "router_nodes"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_location(data):
    url = os.getenv('INVENTORY_URL') + "locations"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_logicalunit(data):
    url = os.getenv('INVENTORY_URL') + "logical_units"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_client_node(data):
    url = os.getenv('INVENTORY_URL') + "client_nodes"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    logging.debug(data)
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_vrf(data):
    url = os.getenv('INVENTORY_URL') + "vrfs"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_portgroup(data):
    url = os.getenv('INVENTORY_URL') + "portgroups"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_virtual_pod(data):
    url = os.getenv('INVENTORY_URL') + "virtualpods"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_vlan_tag(data):
    url = os.getenv('INVENTORY_URL') + "vlans"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def create_access_port_at_access_node(access_node_id, data):
    url = os.getenv('INVENTORY_URL') +"access_nodes/" + str(access_node_id) + "/access_ports"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")

def create_client_port_at_client_node(client_node_sn, data):
    url = os.getenv('INVENTORY_URL') + "client_nodes/"+ str(client_node_sn) + "/client_node_ports"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")

def add_vlan_to_access_node(access_node_id,data):
    url = os.getenv('INVENTORY_URL') + "access_nodes/" + str(access_node_id) + "/vlans"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")




### MODIFY METHODS 
def add_vrf_to_location(location_id,data):
    url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id) + "/vrfs"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


# def add_logicalunit_to_router_node(router_node_id,data):
#     url = os.getenv('INVENTORY_URL') + "router_nodes/" + str(router_node_id) + "/logical_units"
#     token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
#     response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
#     if response.status_code == HTTP_201_CREATED:
#         return response.json()
#     else:
#         raise ServiceException("Unable to create service")


def remove_vlan_from_access_node(access_node_id,vlan_id):
    url = os.getenv('INVENTORY_URL') + "access_nodes/" + str(access_node_id) + "/vlans/" +str(vlan_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def remove_vrf_from_location(location_id,vrf_id):
    url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id) + "/vrfs/" + str(vrf_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def remove_logicalunit_from_router_node(router_node_id,logical_unit_id):
    url = os.getenv('INVENTORY_URL') + "router_nodes/" + str(router_node_id) + "/logical_units/" +str(logical_unit_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response.json()
    else:
        raise ServiceException("Unable to create service")


def release_access_port(access_port_id):
    url = settings.INVENTORY_URL + "access_ports/" + str(access_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":False}
    r = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise AccessPortException("Invalid access port.", status_code=r.status_code)


def use_access_port(access_port_id):
    url= os.getenv('INVENTORY_URL') + "access_ports/" + str(access_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessPortException("Invalid AccessPort")


def use_client_node_port(client_node_id, client_port_id):
    url= os.getenv('INVENTORY_URL') + "client_nodes/" + str(client_node_id) + "/client_node_ports/" + str(client_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = { "used": True }
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientPortException("Unable update client port")


def release_client_node_port(client_node_id, client_port_id):
    url= os.getenv('INVENTORY_URL') + "client_nodes/" + str(client_node_id) + "/client_node_ports/" + str(client_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = { "used": False }
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientPortException("Unable to release client port")


def update_cpe(client_node_sn, data):
    url = os.getenv('INVENTORY_URL') + "client_nodes/" + str(client_node_sn)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientNodeException("Unable to update client node")






### DELETE METHODS 
def delete_access_node(elem_id):
    url = os.getenv('INVENTORY_URL') + "access_nodes/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")

def delete_router_node(elem_id):
    url = os.getenv('INVENTORY_URL') + "router_nodes/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_location(elem_id):
    url = os.getenv('INVENTORY_URL') + "locations/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_logicalunit(elem_id):
    url = os.getenv('INVENTORY_URL') + "logical_units/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_client_node(elem_id):
    url = os.getenv('INVENTORY_URL') + "client_nodes/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_vrf(elem_id):
    url = os.getenv('INVENTORY_URL') + "vrfs/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_portgroup(elem_id):
    url = os.getenv('INVENTORY_URL') + "portgroups/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_virtual_pod(elem_id):
    url = os.getenv('INVENTORY_URL') + "virtualpods/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_vlan_tag(elem_id):
    url = os.getenv('INVENTORY_URL') + "vlans/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")


def delete_access_port(elem_id):
    url = os.getenv('INVENTORY_URL') + "access_ports/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")

def delete_client_port(client_node_sn, elem_id):
    url = os.getenv('INVENTORY_URL') + "client_nodes/" + str(client_node_sn) + "/client_node_ports/"+ str(elem_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_204_NO_CONTENT:
        return response
    else:
        raise ServiceException("Unable to delete service")



### GET METHODS 
def get_location(location_id):
    url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise LocationException("Invalid location")

def get_router_node(router_node_id):
    url= os.getenv('INVENTORY_URL') + "router_nodes/"+ str(router_node_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise RouterNodeException("Invalid Router Node")

def get_virtual_pods(location_id):
    url= os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/virtualpods"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VirtualPodException("Invalid VirtualPod/Location pair")

def get_virtual_pod(location_id, virtual_pod_id):
    url= os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/virtualpods/" + str(virtual_pod_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VirtualPodException("Invalid VirtualPod/Location pair")

def get_client_node(client_node_sn):
    url= os.getenv('INVENTORY_URL') + "client_nodes/" + str(client_node_sn)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise ClientNodeException("Invalid client Node")

def get_virtual_pod_downlink_portgroup(virtual_pod_id):
    url= os.getenv('INVENTORY_URL') + "virtualpods/"+ str(virtual_pod_id) + "/portgroups?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response[0]
    else:
        raise VirtualPodException("Invalid VirtualPod/Location pair")

def use_portgroup(portgroup_id):
    url= os.getenv('INVENTORY_URL') + "portgroups/" + str(portgroup_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise PortgroupException("Invalid Portgroup")

def get_free_logical_units(router_node_id):
    url = os.getenv('INVENTORY_URL') + "router_nodes/" + str(router_node_id) + "/logical_units?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if (r.status_code == HTTP_200_OK):
        return r.json()
    else:
        raise LogicalUnitException("Invalid LogicalUnit")

def add_logical_unit_to_router_node(router_node_id,logical_unit_id,product_id=None):
    url= os.getenv('INVENTORY_URL') + "router_nodes/" + str(router_node_id) + "/logical_units"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"logical_unit_id":logical_unit_id}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_201_CREATED:
        return json_response
    else:
        raise LogicalUnitException("Unable to add LogicalUnit")

def get_free_access_port(location_id):
    url= os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/access_ports?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if (r.status_code == HTTP_200_OK):
        return r.json()
    else:
        raise AccessPortException("Invalid AccessPort/Location pair")


def get_access_node(access_node_id):
    url= os.getenv('INVENTORY_URL') + "access_nodes/"+ str(access_node_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessNodeException("Invalid AccessNode")


def get_client_port(client_node_id, client_port_id):
    url = os.getenv('INVENTORY_URL') + "client_nodes/"  + str(client_node_id) + "/client_node_ports/" + str(client_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientPortException("Invalid ClientNode/ClientPort pair")


def get_vrfs():
    url = os.getenv('INVENTORY_URL') + "vrfs" 
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to retrieve vrfs")



def get_free_cpe_port(client_node_sn):
    url= os.getenv('INVENTORY_URL') + "client_nodes/" + str(client_node_sn) + "/client_node_ports?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if r.status_code == HTTP_200_OK:
        return r.json()[0]
    else:
        raise ClientPortException("Invalid ClientNode/Port pair")


def vrf_exists_in_location(vrf_id,location_id):
    url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id) + "/vrfs/" + str(vrf_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if (r.status_code == HTTP_200_OK):
        return r.json()['exists']
    else:
        raise VrfException("Invalid Vrf/Location pair")

# def add_location_to_vrf(vrf_id,location_id):
#     url = os.getenv('INVENTORY_URL') + "vrfs/" + str(vrf_id) + "/locations/" + str(location_id)
#     token = get_inventory_authentication_token()
#     response = requests.put(url, auth = None, verify = False, headers = rheaders)
#     json_response = json.loads(response.text)
#     if response.status_code == HTTP_200_OK:
#         return json_response
#     else:
#         raise LocationException("Invalid VRF/Location pair")


def get_access_port(access_port_id):
    url= os.getenv('INVENTORY_URL') + "access_ports/"+ str(access_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessPortException("Invalid AccessPort")

def get_vrf(vrf_id):
    url = os.getenv('INVENTORY_URL') + "vrfs/" + str(vrf_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VrfException("Invalid Vrf Id")


def get_client_vrfs(client_name):
    url= os.getenv('INVENTORY_URL') + "vrfs?client="+client_name
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to retrieve Vrf")


def get_free_vrf():
    url= os.getenv('INVENTORY_URL') + "vrfs?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response[0]
    else:
        raise VrfException("Unable to retrieve Vrf")


def use_vrf(vrf_id, vrf_name, client_name):
    url= os.getenv('INVENTORY_URL') + "vrfs/" + vrf_id
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = {"used":True, "name": vrf_name, "client": client_name}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to update Vrf")



def get_free_vlan(access_node_id):
    url = os.getenv('INVENTORY_URL') + "access_nodes/"+ str(access_node_id) + "/vlans?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response[0]
    else:
        raise VlanTagException("Unable to retrieve VlanTag")

def get_free_vlans(access_node_id):
    url = os.getenv('INVENTORY_URL') + "access_nodes/"+ str(access_node_id) + "/vlans?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VlanTagException("Unable to retrieve VlanTag")

def use_vlan(access_node_id, vlan_id):
    url = os.getenv('INVENTORY_URL') + "access_nodes/" + str(access_node_id) + "/vlans"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    data = { 'vlan_tag_id': vlan_id }
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise VlanTagException("Unable to update VlanTag")

def get_device_model(device_model_id):
    url = os.getenv('INVENTORY_URL') + "device_models/" + str(device_model_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
        
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise DeviceModelException("Invalid device model.", status_code=r.status_code)
    else:
        raise DeviceModelException("Unable to fetch device model.", status_code=r.status_code)



def release_vlan(access_node_id, vlan_id):
    url = settings.INVENTORY_URL + "access_nodes/" + str(access_node_id) + "/vlans/" + str(vlan_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.delete(url, auth = None, verify = False, headers = rheaders)

