from django.conf import settings
from jeangrey.exceptions import *
from jeangrey.constants import *

import json
import requests

def get_access_node(access_node_id):
	url = settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id)
	rheaders = {'Content-Type': 'application/json'}
	r = requests.get(url, auth = None, verify = False, headers = rheaders)
	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise AccessNodeException("Invalid Access Node.", status_code=r.status_code)

def get_access_port(access_port_id):
	url = settings.INVENTORY_URL + "accessports/"+ str(access_port_id)
	rheaders = {'Content-Type': 'application/json'}
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

def get_router_node(location_id):
	url = settings.INVENTORY_URL + "locations/" + str(location_id) + "/routernodes"
	rheaders = { 'Content-Type': 'application/json' }
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise LocationException("Invalid location.", status_code=r.status_code)


def get_free_access_port(location_id):
	url = settings.INVENTORY_URL + "locations/"+ str(location_id) + "/accessports?used=false"
	rheaders = {'Content-Type': 'application/json'}
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise LocationException("Invalid location.", status_code=r.status_code)

def get_location_id(location_name):
	url = settings.INVENTORY_URL + "locations?name=" + location_name
	rheaders = { 'Content-Type': 'application/json' }
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()['id']
	else:
		raise LocationException("Could not resolve request", status_code=r.status_code)

def use_port(access_port_id):
	url = settings.INVENTORY_URL + "accessports/" + access_port_id
	rheaders = {'Content-Type': 'application/json'}
	data = {"used":True}
	r = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise AccessPortException("Invalid access port.", status_code=r.status_code)

def get_client_vrfs(client_name):
	url = settings.INVENTORY_URL + "vrfs?client="+client_name
	rheaders = {'Content-Type': 'application/json'}
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise VrfException("Could not resolve request.", status_code=r.status_code)


def get_free_vrf():
	url = settings.INVENTORY_URL + "vrfs?used=False"
	rheaders = {'Content-Type': 'application/json'}
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise VrfException("Could not resolve request.", status_code=r.status_code)


def use_vrf(vrf_id, vrf_name, client_name):
	url = settings.INVENTORY_URL + "vrfs/" + vrf_id
	rheaders = {'Content-Type': 'application/json'}
	data = {"used":True, "name": vrf_name, "client": client_name}
	r = requests.put(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise VrfException("Invalid VRF Id.", status_code=r.status_code)

def get_free_vlan(access_node_id):
	url = settings.INVENTORY_URL + "accessnodes/"+ str(access_node_id) + "/vlantags?used=false"
	rheaders = { 'Content-Type': 'application/json' }
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()[0]
	else:
		raise AccessNodeException("Invalid access node.", status_code=r.status_code)

def use_vlan(access_node_id, vlan_id):
	url = settings.INVENTORY_URL + "accessnodes/" + str(access_node_id) + "/vlantags"
	rheaders = { 'Content-Type': 'application/json' }
	data = { 'vlan_id': vlan_id }
	r = requests.post(url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise AccessNodeException("Invalid access node.", status_code=r.status_code)

def get_vrf(vrf_name):
	url = settings.INVENTORY_URL + "vrfs?name="+ vrf_name
	rheaders = { 'Content-Type': 'application/json' }
	r = requests.get(url, auth = None, verify = False, headers = rheaders)

	if r.json() and r.status_code == HTTP_200_OK:
		return r.json()
	else:
		raise VrfException("Invalid VRF Id.", status_code=r.status_code)