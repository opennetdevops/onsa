from charles.constants import *
from charles.exceptions import *

import requests
import json
import os
import logging
import coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def configure_service(config):
    url = os.getenv('WORKER_URL') + "services"
    rheaders = {'Content-Type': 'application/json'}
    data = config
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

def get_ipam_authentication_token():
    url = "/api/authenticate"
    rheaders = {'Content-Type': 'application/json'}
    #App User - todo change
    data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
    response = requests.post(os.getenv('IPAM_URL') + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    logging.debug(response.text)
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

def get_location(location_id):
    url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise LocationException("Invalid location")

def get_router_node(router_node_id):
    url= os.getenv('INVENTORY_URL') + "routernodes/"+ str(router_node_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise RouterNodeException("Invalid Router Node")

def get_virtual_pods(location_id):
    url= os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/virtualpods"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VirtualPodException("Invalid VirtualPod/Location pair")

def get_virtual_pod(location_id, virtual_pod_id):
    url= os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/virtualpods/" + str(virtual_pod_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VirtualPodException("Invalid VirtualPod/Location pair")

def get_client_node(client_node_sn):
    url= os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_sn)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise ClientNodeException("Invalid client Node")

def get_virtual_pod_downlink_portgroup(virtual_pod_id):
    url= os.getenv('INVENTORY_URL') + "virtualpods/"+ str(virtual_pod_id) + "/portgroups?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response[0]
    else:
        raise VirtualPodException("Invalid VirtualPod/Location pair")

def use_portgroup(portgroup_id):
    url= os.getenv('INVENTORY_URL') + "portgroups/" + str(portgroup_id)
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise PortgroupException("Invalid Portgroup")

def get_free_logical_units(router_node_id):
    url = os.getenv('INVENTORY_URL') + "routernodes/" + str(router_node_id) + "/logicalunits?used=false"
    rheaders = {'Content-Type': 'application/json'}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if (r.status_code == HTTP_200_OK):
        return r.json()
    else:
        raise LogicalUnitException("Invalid LogicalUnit")

def add_logical_unit_to_router_node(router_node_id,logical_unit_id,product_id):
    url= os.getenv('INVENTORY_URL') + "routernodes/" + str(router_node_id) + "/logicalunits"
    rheaders = {'Content-Type': 'application/json'}
    data = {"logical_unit_id":logical_unit_id,
                    "product_id":product_id}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_201_CREATED:
        return json_response
    else:
        raise LogicalUnitException("Unable to add LogicalUnit")

def get_free_access_port(location_id):
    url= os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/accessports?used=false"
    rheaders = {'Content-Type': 'application/json'}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if (r.status_code == HTTP_200_OK):
        return r.json()
    else:
        raise AccessPortException("Invalid AccessPort/Location pair")

def use_port(access_port_id):
    url= os.getenv('INVENTORY_URL') + "accessports/" + str(access_port_id)
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessPortException("Invalid AccessPort")

def release_access_port(access_port_id):
    url= os.getenv('INVENTORY_URL') + "accessports/" + str(access_port_id)
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":False}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessPortException("Invalid AccessPort")

def get_access_node(access_node_id):
    url= os.getenv('INVENTORY_URL') + "accessnodes/"+ str(access_node_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessNodeException("Invalid AccessNode")

def get_free_vlan_tag(access_port_id):
    url= os.getenv('INVENTORY_URL') + "accessnodes/"+ str(access_port_id) + "/vlantags?used=false"
    rheaders = {'Content-Type': 'application/json'}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if (r.status_code == HTTP_200_OK):
        return r.json()
    else:
        raise VlanTagException("Invalid AccessPort/VlanTag pair")

def add_vlan_tag_to_access_node(vlan_tag,access_node_id,access_port_id,service_id,client_node_sn,client_node_port,bandwidth,vrf_id=None):
    url= os.getenv('INVENTORY_URL') + "accessnodes/"+ str(access_node_id) + "/vlantags"
    rheaders = {'Content-Type': 'application/json'}
    data = {"vlan_tag":vlan_tag,
                    "service_id":service_id,
                    "client_node_sn":client_node_sn,
                    "client_node_port":client_node_port,
                    "bandwidth":bandwidth,
                    "access_port_id":access_port_id,
                    "vrf_id": vrf_id}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_201_CREATED:
        return json_response
    else:
        raise VlanTagException("Unable to add VlanTag to AccessNode")

def update_service(service_id, data):
    url = os.getenv('JEAN_GREY_URL') + "services/" + str(service_id)
    rheaders = {'Content-Type': 'application/json'}

    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise ServiceException("Unable to update service")

def get_access_port(access_port_id):
    url= os.getenv('INVENTORY_URL') + "accessports/"+ str(access_port_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise AccessPortException("Invalid AccessPort")

def get_vrf(vrf_id):
    url = os.getenv('INVENTORY_URL') + "vrfs/" + str(vrf_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise VrfException("Invalid Vrf Id")

def vrf_exists_in_location(vrf_id,location_id):
    url = os.getenv('INVENTORY_URL') + "vrfs/" + str(vrf_id) + "/locations/" + str(location_id)
    rheaders = {'Content-Type': 'application/json'}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)

    if (r.status_code == HTTP_200_OK):
        return r.json()['exists']
    else:
        raise VrfException("Invalid Vrf/Location pair")

def add_location_to_vrf(vrf_id,location_id):
    url = os.getenv('INVENTORY_URL') + "vrfs/" + str(vrf_id) + "/locations/" + str(location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.put(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise LocationException("Invalid VRF/Location pair")


def rollback_service(service_id):
    url = "/api/products/" + service_id + "/rollback"
    response = requests.post(url)
    json_response = json.loads(response.text)
    if response.status_code == HTTP_200_OK:
        return json_response
    else:
        raise ServiceException("Unable to rollback service")


def update_core_service_status(service_id, data):
    rheaders = {'Content-Type': 'application/json'}
    url = os.getenv('CORE_URL') +"services/" + str(service_id)
    response = requests.put(url, data = json.dumps(data), headers=rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ServiceException("Unable to update core service")


def get_free_cpe_port(client_node_sn):
    url= os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_sn) + "/clientports?used=False"
    rheaders = {'Content-Type': 'application/json'}
    r = requests.get(url, auth = None, verify = False, headers = rheaders)
    if r.status_code == HTTP_200_OK:
        return r.json()[0]
    else:
        raise ClientPortException("Invalid ClientNode/Port pair")

def update_cpe(client_node_sn, data):
    url = os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_sn)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientNodeException("Unable to update client node")

def get_service(service_id):
    url = os.getenv('JEAN_GREY_URL') + "services/" + str(service_id)
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


def get_client_port(client_node_id, client_port_id):
    url = os.getenv('INVENTORY_URL') + "clientnodes/"  + str(client_node_id) + "/clientports/" + str(client_port_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientPortException("Invalid ClientNode/ClientPort pair")


def use_port(client_node_id, client_port_id):
    url= os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)
    rheaders = { 'Content-Type': 'application/json' }
    data = { "used": True }
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientPortException("Unable update client port")


def release_client_node_port(client_node_id, client_port_id):
    url= os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)
    rheaders = { 'Content-Type': 'application/json' }
    data = { "used": False }
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise ClientPortException("Unable to release client port")

def get_vrfs():
    url = os.getenv('INVENTORY_URL') + "vrfs" 
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to retrieve vrfs")

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
        use_port(client_node_sn, cpe_port_id)
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



def get_client_vrfs(client_name):
    url= os.getenv('INVENTORY_URL') + "vrfs?client="+client_name
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to retrieve Vrf")




def get_free_vrf():
    url= os.getenv('INVENTORY_URL') + "vrfs?used=False"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response[0]
    else:
        raise VrfException("Unable to retrieve Vrf")




def use_vrf(vrf_id, vrf_name, client_name):
    url= os.getenv('INVENTORY_URL') + "vrfs/" + vrf_id
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True, "name": vrf_name, "client": client_name}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_200_OK:
        return response.json()
    else:
        raise VrfException("Unable to update Vrf")




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


def get_free_vlan(access_node_id):
    url = os.getenv('INVENTORY_URL') + "accessnodes/"+ str(access_node_id) + "/vlantags?used=false"
    rheaders = { 'Content-Type': 'application/json' }
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response and response.status_code == HTTP_200_OK:
        return json_response[0]
    else:
        raise VlanTagException("Unable to retrieve VlanTag")

def use_vlan(access_node_id, vlan_id):
    url = os.getenv('INVENTORY_URL') + "accessnodes/" + str(access_node_id) + "/vlantags"
    rheaders = { 'Content-Type': 'application/json' }
    data = { 'vlan_id': vlan_id }
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    if response.status_code == HTTP_201_CREATED:
        return response.json()
    else:
        raise VlanTagException("Unable to update VlanTag")

