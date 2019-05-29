from charles.constants import *
from charles.exceptions import *
from charles.models import Service

import requests
import json
import os
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_ipam_authentication_token():
    url = "/api/authenticate"
    rheaders = {'Content-Type': 'application/json'}
    #App User - todo change
    data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
    response = requests.post(os.getenv('IPAM_URL') + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    # logging.debug(response.text)
    return json.loads(response.text)['auth_token']


def get_ip_wan_nsx(location, client_name, service_id):
    url = os.getenv('IPAM_URL') + "/api/networks/assign_ip"

    token = get_ipam_authentication_token()

    rheaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    #TODO Modify constant WAN_NSX
    data = { "description" : client_name + "-" + service_id, "owner" : "WAN_NSX_" + location, "ip_version" : 4 }
 
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    
    if "network" in json_response:
        return json_response["network"]
    else:
        raise IPAMException("No available IP on network")

def get_wan_mpls_network(location,client_name,service_id):
    #Default prefix set by IDR
    mask = 30
    description = client_name + "-" + str(service_id)
    owner = "WAN_MPLS_" + location
    token = get_ipam_authentication_token()
    url = os.getenv('IPAM_URL') + "/api/networks/assign_subnet"
    rheaders = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token}
    data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if "network" in json_response:
        return json_response["network"]
    else:
        raise IPAMException("No available subnet")

def get_client_network(client_name,service_id,mask):
    description = client_name + "-" + str(service_id)
    owner = "PUBLIC_ONSA"
    token = get_ipam_authentication_token()
    url = os.getenv('IPAM_URL') + "/api/networks/assign_subnet"
    rheaders = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token}
    data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if "network" in json_response:
        return json_response["network"]
    else:
        raise IPAMException("No available IP/Subnet")

def get_subnets_by_description(description):
    token = get_ipam_authentication_token()
    url = os.getenv('IPAM_URL') + "/api/networks?description=" + description
    rheaders = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise IPAMException("Not subnets in provided description")

def release_ip(client_name,product_id):
    description = client_name + "-" + str(product_id)
    subnet = get_subnets_by_description(description)[0]
    subnet_id = subnet['id']
    token = get_ipam_authentication_token()
    url = os.getenv('IPAM_URL') + "/api/networks/" + str(subnet_id) + "/release"
    rheaders = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return None
    else:
        raise IPAMException("Unable to release IP")


def destroy_subnet(client_name,product_id):
    description = client_name + "-" + str(product_id)
    subnet_to_destroy = get_subnets_by_description(description)[0]
    subnet_id = subnet['id']
    token = get_ipam_authentication_token()
    url = os.getenv('IPAM_URL') + "/api/networks/" + str(subnet_id)
    rheaders = {'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return None
    else:
        raise IPAMException("Unable to destroy subnet")
