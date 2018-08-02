import jinja2
from ..common.render import render

from netmiko import ConnectHandler
from jinja2 import Template

import requests


from pprint import pprint

import json

import ipaddress
import os


class TransitionHandler(object):

	def __init__(self, host):
		self.my_device = {
		'host': host,
		'username': "lab",
		'password': "lab123",
		'device_type': 'cisco_ios',
		'global_delay_factor': 1
		}


		self.path = "../../templates/transition/"

	def _generate_params(self, params):


		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']

		pprint(params)

		lines = open(self.path,'r').read().splitlines()

		config = []

		for line in lines:
			template = Template(line)
			config.append(template.render(**params))

		print(config)

		return config

	
	def configure_tn(self, method, model, params):

		self.path += model

		dir = os.path.dirname(__file__)

		net_connect = ConnectHandler(**self.my_device)

		if net_connect is None:
			return False

		if method == "set":
			self.path += "/set.conf"

		elif method == "delete":
			self.path += "/delete.conf"

		self.path = os.path.join(dir, self.path)

		print(self.path)

		config = self._generate_params(params)



		output = net_connect.send_config_set(config)

		print(output)
		
		# Clossing connection    
		net_connect.disconnect()

		return True # ToDo: Catch error if configuration failed
		