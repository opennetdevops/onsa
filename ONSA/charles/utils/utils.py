from django.conf import settings
from pprint import pprint
import requests
import json

def configure_service(config):
    url = settings.WORKER_URL + "services"
    rheaders = {'Content-Type': 'application/json'}
    data = config
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

def get_ipam_authentication_token():
    url = "/api/authenticate"
    rheaders = {'Content-Type': 'application/json'}
    #App User
    data = {"email":"malvarez@lab.fibercorp.com.ar", "password":"Matias.2015"}
    response = requests.post(settings.IPAM_URL + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    return json.loads(response.text)['auth_token']


def get_ip_wan_nsx(location, client_name, service_id):
    url = settings.IPAM_URL + "/api/networks/assign_ip"

    token = get_ipam_authentication_token()

    rheaders = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    data = { "description" : client_name + "-" + service_id, "owner" : "WAN_NSX_" + location, "ip_version" : 4 }
 
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    
    print(json_response)

    if "network" in json_response:
        return json_response["network"]
    else:
        return None

def get_wan_mpls_network(location,client_name,service_id):
    #Default prefix set by IDR
    mask = 30
    description = client_name + "-" + service_id
    owner = "WAN_MPLS_" + location
    token = get_ipam_authentication_token()
    url = settings.IPAM_URL + "/api/networks/assign_subnet"
    rheaders = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token}
    data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if "network" in json_response:
        return json_response["network"]
    else:
        return None

def get_client_network(client_name,service_id,mask):
    description = client_name + "-" + service_id
    owner = "PUBLIC_ONSA"
    token = get_ipam_authentication_token()
    url = settings.IPAM_URL + "/api/networks/assign_subnet"
    rheaders = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token}
    data = {"description":description,"owner":owner,"ip_version":4,"mask":mask}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if "network" in json_response:
        return json_response["network"]
    else:
        return None

def get_subnets_by_description(description):
    token = get_ipam_authentication_token()
    url = settings.IPAM_URL + "/api/networks?description=" + description
    rheaders = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    return json_response

def release_ip(client_name,product_id):
    description = client_name + "-" + product_id
    subnet = _get_subnets_by_description(description)[0]
    subnet_id = subnet['id']
    token = get_ipam_authentication_token()
    url = settings.IPAM_URL + "/api/networks/" + str(subnet_id) + "/release"
    rheaders = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, auth = None, verify = False, headers = rheaders)

def destroy_subnet(client_name,product_id):
    description = client_name + "-" + product_id
    subnet_to_destroy = _get_subnets_by_description(description)[0]
    subnet_id = subnet['id']
    token = get_ipam_authentication_token()
    url = settings.IPAM_URL + "/api/networks/" + str(subnet_id)
    rheaders = {'Authorization': 'Bearer ' + token}
    response = requests.delete(url, auth = None, verify = False, headers = rheaders)

def get_location(location_id):
    url = settings.INVENTORY_URL + "locations/" + str(location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_router_node(router_node_id):
    url= settings.INVENTORY_URL + "routernodes/"+ str(router_node_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_virtual_pods(location_id):
    url= settings.INVENTORY_URL + "locations/"+ str(location_id) + "/virtualpods"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_virtual_pod(location_id, virtual_pod_id):
    url= settings.INVENTORY_URL + "locations/"+ str(location_id) + "/virtualpods/" + str(virtual_pod_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_client_node(client_node_sn):
    url= settings.INVENTORY_URL + "clientnodes/" + str(client_node_sn)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_virtual_pod_downlink_portgroup(virtual_pod_id):
    url= settings.INVENTORY_URL + "virtualpods/"+ str(virtual_pod_id) + "/portgroups?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def use_portgroup(portgroup_id):
    url= settings.INVENTORY_URL + "portgroups/" + str(portgroup_id)
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_free_logical_units(router_node_id):
    url = settings.INVENTORY_URL + "routernodes/" + str(router_node_id) + "/logicalunits?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    #TODO check minimum size = 2
    if json_response:
        return json_response
    else:
        return None

def add_logical_unit_to_router_node(router_node_id,logical_unit_id,product_id):
    url= settings.INVENTORY_URL + "routernodes/" + str(router_node_id) + "/logicalunits"
    rheaders = {'Content-Type': 'application/json'}
    data = {"logical_unit_id":logical_unit_id,
                    "product_id":product_id}
    response = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_free_access_port(location_id):
    url= settings.INVENTORY_URL + "locations/"+ str(location_id) + "/accessports?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def use_port(access_port_id):
    url= settings.INVENTORY_URL + "accessports/" + str(access_port_id)
    rheaders = {'Content-Type': 'application/json'}
    data = {"used":True}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_access_node(access_node_id):
    url= settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_free_vlan_tag(access_port_id):
    url= settings.INVENTORY_URL + "accessnodes/"+ str(access_port_id) + "/vlantags?used=false"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def add_vlan_tag_to_access_node(vlan_tag,access_node_id,access_port_id,service_id,client_node_sn,client_node_port,bandwidth,vrf_id=None):
    url= settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags"
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
    if json_response:
        return json_response
    else:
        return None

def update_service(service_id, data):
    url = settings.JEAN_GREY_URL + "services/" + str(service_id)
    rheaders = {'Content-Type': 'application/json'}

    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_access_port(access_port_id):
    url= settings.INVENTORY_URL + "accessports/"+ str(access_port_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_vrf(vrf_id):
    url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def vrf_exists_in_location(vrf_id,location_id):
    url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id) + "/locations/" + str(location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response["exists"]
    else:
        return None

def add_location_to_vrf(vrf_id,location_id):
    url = settings.INVENTORY_URL + "vrfs/" + str(vrf_id) + "/locations/" + str(location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.put(url, auth = None, verify = False, headers = rheaders)

def rollback_service(service_id):
    url = "/api/products/" + service_id + "/rollback"
    r = requests.post(url)

def update_core_service_status(service_id, data):
    rheaders = {'Content-Type': 'application/json'}
    url = settings.CORE_URL +"services/" + str(service_id)
    r = requests.put(url, data = json.dumps(data), headers=rheaders)

def get_free_cpe_port(client_node_sn):
    url= settings.INVENTORY_URL + "clientnodes/" + str(client_node_sn) + "/clientports?used=False"
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response[0]
    else:
        return None

def update_cpe(client_node_sn, data):
    url = settings.INVENTORY_URL + "clientnodes/" + str(client_node_sn)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_service(service_id):
    url = settings.JEAN_GREY_URL + "services/" + str(service_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_client(client_id):
    url = settings.JEAN_GREY_URL + "clients/"  + str(client_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


def get_client_port(client_node_id, client_port_id):
    url = settings.INVENTORY_URL + "clientnodes/"  + str(client_node_id) + "/clientports/" + str(client_port_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


def use_port(client_node_id, client_port_id):
    url= settings.INVENTORY_URL + "clientnodes/" + str(client_node_id) + "/clientports/" + str(client_port_id)

    rheaders = { 'Content-Type': 'application/json' }
    data = { "used": True }
    response = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
    
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_vrfs():
    url = settings.INVENTORY_URL + "vrfs" 
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None

def get_customer_location(client_id, customer_location_id):
    url = settings.JEAN_GREY_URL + "clients/"  + str(client_id) +"/customerlocations/" + str(customer_location_id)
    rheaders = {'Content-Type': 'application/json'}
    response = requests.get(url, auth = None, verify = False, headers = rheaders)
    json_response = json.loads(response.text)
    if json_response:
        return json_response
    else:
        return None


def fetch_cpe(service, client, customer_location):
    client_node = get_client_node(service['client_node_sn'])
    """
    Update Inventory with CPE data if needed
    """
    if client_node['client'] is None:
        cpe_data = { 'client': client['name'], 'customer_location': customer_location['address'] }
        update_cpe(service['client_node_sn'], cpe_data)

    """
    Get free CPE port from Inventory and
    mark it as a used port.
    """
    cpe_port = get_free_cpe_port(service['client_node_sn'])
    cpe_port_id = cpe_port['id']

    #Assign CPE Port (mark as used)
    use_port(service['client_node_sn'], cpe_port_id)

    return cpe_port_id
