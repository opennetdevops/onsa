from django.conf import settings
from django.contrib.auth.models import User
from pprint import pprint

import json
import requests
import ldap

def pop_empty_keys(d):
	return {k: v for k, v in d.items() if v is not None}

def get_router_node(router_node_id):
	url = os.getenv('INVENTORY_URL') + "routernodes/" + router_node_id
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_access_node(access_node_id):
	url = os.getenv('INVENTORY_URL') + "accessnodes/" + str(access_node_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_access_port(access_port_id):
	url = os.getenv('INVENTORY_URL') + "accessports/" + str(access_port_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_client(client_id):
	url = os.getenv('JEAN_GREY_URL') + "clients/" + str(client_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_client_node(client_node_id):
	url = os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_client_port(client_node_sn, client_port_id):
	url = os.getenv('INVENTORY_URL') + "clientnodes/" + str(client_node_sn) + "/clientports/" + str(client_port_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None


def get_free_access_port(location_id):
	url = os.getenv('INVENTORY_URL') + "locations/"+ str(location_id) + "/accessports?used=false"
	rheaders = {'Content-Type': 'application/json'}
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response[0]
	else:
		return None


def get_vrf(vrf_name):
	url = os.getenv('INVENTORY_URL') + "vrfs?name="+ vrf_name
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)
	if json_response:
		return json_response
	else:
		return None

def get_service(service_id):
	url = os.getenv('JEAN_GREY_URL') + "services/" + str(service_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)

	return json_response

def get_location(location_id):
	url = os.getenv('INVENTORY_URL') + "locations/" + str(location_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)

	return json_response

def get_customer_location(client_id, cl_id):
	url = os.getenv('JEAN_GREY_URL') + "clients/" + str(client_id) + "/customerlocations/" + str(cl_id)
	rheaders = { 'Content-Type': 'application/json' }
	response = requests.get(url, auth = None, verify = False, headers = rheaders)
	json_response = json.loads(response.text)

	return json_response

def authenticate_ldap(username, password):
	host = "ldap://10.120.78.5"
	dn = "cn=fc__netauto,ou=OU Aplicaciones,ou=OU Hornos,dc=lab,dc=fibercorp,dc=com,dc=ar"
	passw = 'F1b3rc0rp!'

	# Init LDAP Object
	l = ldap.initialize(host)
	l.set_option(ldap.OPT_REFERRALS, 0)
	l.protocol_version = 3
	
	# Bind query user
	l.simple_bind_s(dn,passw)

	# Authenticate user
	base = "dc=lab,dc=fibercorp,dc=com,dc=ar"
	scope = ldap.SCOPE_SUBTREE
	filter = "(sAMAccountName=" + username + ")"
	attrs = ["sAMAccountName"]
	r = l.search_s(base, scope, filter, attrs)
	user_dn = r[0][0]

	try:
		l.simple_bind_s(user_dn, password)
		username = r[0][1]['sAMAccountName'][0].decode("utf-8")
		user = User(username=username, is_active=True)	

	except ldap.INVALID_CREDENTIALS:
		return None
			
	return user