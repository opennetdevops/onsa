import os
import ipaddress
import requests
import json
import logging

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

from requests.exceptions import HTTPError

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import CommitError, RpcTimeoutError, ConnectError, ConnectAuthError, ConfigLoadError

from jinja2 import Template
from pprint import pprint
from .nsx.nsx_rest import *
from .common.render import render
from time import sleep


def get_edge_id_by_name(name, **kwargs):
	rheaders = {'Accept': 'application/json'}

	r = requests.get(kwargs['manager'] + "/api/4.0/edges", auth=(USER, PASS), verify=False, headers=rheaders)
	r.raise_for_status()

	r_dict = json.loads(r.text)	
	allEdges = r_dict['edgePage']['data']

	for edge in allEdges:
		if edge['name'] == name:
			return edge['id']

	return ""


class ConfigHandler:

	def pyez(template_path, parameters):
		
		# print(render(template_path, parameters))

		logging.basicConfig(level=logging.INFO)
		dev = Device(host=parameters['mgmt_ip'], user="lab", password="lab123", port=443)
		dev.bind(cu=Config)

		try:
			logging.info("Openning NETCONF connection to device")
			dev.open()
		except (ConnectError, ConnectAuthError) as err:
			logging.error("Cannot connect to device:%s", err)


		logging.info("Locking the configuration")
		try:
			dev.cu.lock()
		except LockError:
			logging.error("Error: Unable to lock configuration")
			dev.close()
			return False
		try:
			dev.cu.load(template_path=template_path, merge=True, template_vars=parameters, format="set")
			dev.cu.pdiff()
		except ValueError as err:
			logging.error("Error: %s", err.message)
		except ConfigLoadError as err:
			logging.error("Unable to load configuration changes: %s", err)

			logging.info("Unlocking the configuration")
			try:
				dev.cu.unlock()
			except UnlockError:
				logging.error("Error: Unable to unlock configuration")
			
			dev.close()
			return False


		logging.info("Committing the configuration")
		try:
			dev.timeout=120
			commit_result = dev.cu.commit()
			# Show that the commit worked True means it worked, false means it failed
			logging.debug( "Commit result: %s",commit_result)
		except (CommitError, RpcTimeoutError) as e:
			logging.error( "Error: Unable to commit configuration")
			print(e)
			dev.cu.unlock()
			dev.close()
			return False

		logging.info( "Unlocking the configuration")
		try:
			 dev.cu.unlock()
		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")

		try:
			logging.info("Closing NETCONF session")
			dev.close()
		except ConnectClosedError as err:
			logging.info("Error: Unable to close connection. %s", err)

		return True


	def ssh(template_path, params):

		my_device = {
		'host': params['mgmt_ip'],
		'username': "lab",
		'password': "lab123",
		'device_type': 'cisco_ios',
		'global_delay_factor': 1
		}

		config = render(template_path, params).splitlines()

		try:
			net_connect = ConnectHandler(**my_device)
			output = net_connect.send_config_set(config)
	    
			net_connect.disconnect()		
			status = True
	
		except (NetMikoTimeoutException, NetMikoAuthenticationException):
			status = False

		return status
		

	def nsx(template_path, params):

		MANAGER = 'https://' + params['mgmt_ip'] 
		params['trigger'] = False
		data = render(template_path, params)


		print(data)

		status = True

		try:
			rheaders = {'Content-Type': 'application/xml'}
			r = requests.post(MANAGER + "/api/4.0/edges", data=data, auth=(USER, PASS), verify=False, headers=rheaders)
			r.raise_for_status()

			sleep(45)
			
			edge_id = get_edge_id_by_name(params['edge_name'], manager=MANAGER)

			params['trigger'] = True
			data = render(template_path, params)

			rheaders = {'Content-Type': 'application/json'}
			r = requests.put(MANAGER + "/api/4.0/edges/%s/routing/config/static" % edge_id, data=data, auth=(USER, PASS), verify=False, headers=rheaders)
			r.raise_for_status()

		except HTTPError:
			print("FAILED!")
			status = False

		return status