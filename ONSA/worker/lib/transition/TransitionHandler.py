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

	def __init__(self, host, model):
		self.my_device = {
		'host': host,
		'username': "lab",
		'password': "lab123",
		'device_type': 'cisco_ios',
		}
		self.path = "../../templates/transition/%s/" % model

	def _generate_params(self, params):
		lines = open(path,'r').read().splitlines()

		config = []

		for line in lines:
			template = Template(line)
			config.append(template.render(**params))

		return config

	
	def configure_tn(self, method, params):
		net_connect = ConnectHandler(**self.my_device)

		if method == "set":
			self.path += "set.conf"

		elif method == "delete":
			self.path += "delete.conf"

		config = self._generate_params(params)

		net_connect.send_config_set(config)
		
		# Clossing connection    
		net_connect.disconnect()

		return True # ToDo: Catch error if configuration failed
		