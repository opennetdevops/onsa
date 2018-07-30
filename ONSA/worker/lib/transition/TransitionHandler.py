import jinja2
from ..common.render import render

from netmiko import ConnectHandler

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

	def _generate_params(self):
		pass

	
	def configure_tn(self, method):
		net_connect = ConnectHandler(**self.my_device)

		if method == "set":
			self.path += "set.conf"

		elif method == "delete":
			self.path += "delete.conf"

		# Clossing connection    
		net_connect.disconnect()
		pass
		