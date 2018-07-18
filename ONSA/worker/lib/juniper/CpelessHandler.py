from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import jinja2
import logging, sys

from pprint import pprint

from .Handler import Handler

class CpelessHandler(Handler):
	def __init__(self, service_type):
		self.path = "../templates/mx104/cpeless/%s/" % service_type

	def _generate_params(method, parameters):
		dir = os.path.dirname(__file__)
		if method == "set":			
			jinja_vars = {
							"sco_ae_interface" : parameters['sco_ae_interface'],
							"sco_logical_unit" : parameters['sco_logical_unit'],
							"sco_interface_description" : "",
							"vrf_name" : parameters["vrf_name"],
							"qinqOuterVlan" : parameters['qinqOuterVlan'],
							"qinqInnerVlan" : parameters['qinqInnerVlan'],
							"public_cidr" : parameters['public_cidr']
						}
			
			self.path += "set.conf"

		elif method == "delete":

			jinja_vars = {
							"sco_ae_interface" : parameters['sco_ae_interface'],
							"sco_logical_unit" : parameters['sco_logical_unit'],
							"vrf_name" : parameters["vrf_name"]
						}

			self.path += "delete.conf"

		template = os.path.join(dir, self.path)

		return "SUCCESS", template, jinja_vars