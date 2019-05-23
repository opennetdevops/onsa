from django.conf import settings
from django.contrib.auth.models import User

from core.constants import *
from core.exceptions import *

import json
import requests
import ldap
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_inventory_authentication_token():
    url = "authenticate"
    rheaders = {'Content-Type': 'application/json'}
    data = {"email":os.getenv('INVENTORY_USER'), "password":os.getenv('INVENTORY_PASSWORD')}
    response = requests.post(os.getenv('INVENTORY_URL') + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    logging.debug(response.text)
    return json.loads(response.text)['auth_token']

def pop_empty_keys(d):
    return {k: v for k, v in d.items() if v is not None}

def get_router_node(router_node_id):
    url = settings.INVENTORY_URL + "router_nodes/" + str(router_node_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
        
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise RouterNodeException("Invalid router node.", status_code=r.status_code)
    else:
        raise RouterNodeException("Unable to fetch router node.", status_code=r.status_code)

def get_router_node_from_location(location_id):
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


def get_client(client_id):
    url = settings.JEAN_GREY_URL + "clients/" + str(client_id)
    rheaders = { 'Content-Type': 'application/json' }
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise ClientException("Invalid client.", status_code=r.status_code)
    else:
        raise ClientException("Unable to fetch client.", status_code=r.status_code)

def get_client_node(client_node_id):
    url = settings.INVENTORY_URL + "clientnodes/" + str(client_node_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise ClientNodeException("Invalid client node.", status_code=r.status_code)
    else:
        raise ClientNodeException("Unable to fetch client node.", status_code=r.status_code)

def get_client_port(client_node_sn, client_port_id):
    url = settings.INVENTORY_URL + "clientnodes/" + str(client_node_sn) + "/clientports/" + str(client_port_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    # TODO: how to raise exception client_node_sn or client_port_id ?
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise ClientPortException("Invalid client.", status_code=r.status_code)
    else:
        raise ClientPortException("Unable to fetch client.", status_code=r.status_code)

def get_device_model(device_model_id):
    url = settings.INVENTORY_URL + "device_models/" + str(device_model_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
        
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise DeviceModelException("Invalid device model.", status_code=r.status_code)
    else:
        raise DeviceModelException("Unable to fetch device model.", status_code=r.status_code)

def get_free_access_port(location_id):
    url = settings.INVENTORY_URL + "locations/"+ str(location_id) + "/access_ports?used=false"
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    print(r.json())
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()[0]
    elif not r.json():
        raise LocationException("Not available AccessPort", status_code=HTTP_503_SERVICE_UNAVAILABLE)
    else:
        raise LocationException("Invalid location.", status_code=r.status_code)


def get_vrf(vrf_name):
    url = settings.INVENTORY_URL + "vrfs?name="+ vrf_name
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    else:
        raise VrfException("Invalid VRF Id.", status_code=r.status_code)

def get_service(service_id):
    url = settings.JEAN_GREY_URL + "services/" + str(service_id)
    rheaders = { 'Content-Type': 'application/json' }
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    
    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise ServiceException("Invalid service.", status_code=r.status_code)
    else:
        raise ServiceException("Unable to fetch service.", status_code=r.status_code)

def get_location(location_id):
    url = settings.INVENTORY_URL + "locations/" + str(location_id)
    token = get_inventory_authentication_token()
    rheaders = { 'Content-Type': 'application/json' , 'Authorization': 'Bearer ' + token}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise LocationException("Invalid location.", status_code=r.status_code)
    else:
        raise LocationException("Unable to fetch location.", status_code=r.status_code)

def get_customer_location(client_id, cl_id):
    url = settings.JEAN_GREY_URL + "clients/" + str(client_id) + "/customerlocations/" + str(cl_id)
    rheaders = { 'Content-Type': 'application/json' }
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if r.json() and r.status_code == HTTP_200_OK:
        return r.json()
    elif r.status_code == HTTP_404_NOT_FOUND:
        raise CustomerLocationException("Invalid customer location.", status_code=r.status_code)
    else:
        raise CustomerLocationException("Unable to fetch customer location.", status_code=r.status_code)

def authenticate_ldap(username, password):
    l = init_ldap()

    r = search_user_ldap(l,username)

    user_dn = r[0][0]
    if user_dn is None:
        return None

    try:
        l.simple_bind_s(user_dn, password)
        username = r[0][1]['userPrincipalName'][0].decode("utf-8")
        
        return User(username=username, is_active=True)	

    except ldap.INVALID_CREDENTIALS:
        return None

def search_user_ldap(l, username):
    # Authenticate user
    base = "dc=lab,dc=fibercorp,dc=com,dc=ar"
    scope = ldap.SCOPE_SUBTREE
    filter = "(userPrincipalName=" + username + ")"
    attrs = ["userPrincipalName"]
    r = l.search_s(base, scope, filter, attrs)
    
    return r

def init_ldap():
    host = "ldap://10.120.78.5"
    dn = "cn=fc__netauto,ou=OU Aplicaciones,ou=OU Hornos,dc=lab,dc=fibercorp,dc=com,dc=ar"
    passw = 'F1b3rc0rp!'

    # Init LDAP Object
    l = ldap.initialize(host)
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.protocol_version = 3

    # Bind query user
    l.simple_bind_s(dn,passw)

    return l

def search_user(username):
    l = init_ldap()

    r = search_user_ldap(l,username)
    user_dn = r[0][0]

    if user_dn is None:
        return None
    else:
        return User(username=username, is_active=True)

def delete_charles_service(service_id):
    url = settings.CHARLES_URL + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    r = requests.delete(url, auth = None, verify = False, headers = rheaders)

    if r.json():
        return r.json()
    else:
        return None

def delete_jeangrey_service(service_id):
    url = settings.JEAN_GREY_URL + "services/"  + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    r = requests.delete(url, auth = None, verify = False, headers = rheaders)

    if r.json():
        return r.json()
    else:
        return None