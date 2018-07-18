from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import jinja2
import logging, sys

from pprint import pprint

from .Handler import Handler

class VcpeHandler(Handler):
	def __init__(self, service_type):
		self.path = "../../templates/mx104/vcpe/%s/" % service_type

	def _generate_params(method, parameters):
		dir = os.path.dirname(__file__)
		if method == "set":			
			jinja_vars = {
							"bridge_domain_id" : "",
							"bridge_domain_description" : "",
							"vxrail_ae_interface" : parameters['vxrail_ae_interface'],
							"vxrail_logical_unit" : parameters['vxrail_logical_unit'],
							"sco_ae_interface" : parameters['sco_ae_interface'],
							"sco_logical_unit" : parameters['sco_logical_unit'],
							"vxrail_interface_description" : "",
							"sco_interface_description" : "",
							"vxrail_vlan" : parameters['vxrail_vlan'],
							"qinqOuterVlan" : parameters['qinqOuterVlan'],
							"qinqInnerVlan" : parameters['qinqInnerVlan'],
							"public_cidr" : parameters['public_cidr']
						}
			
			self.path += "set.conf"

		elif method == "delete":

			jinja_vars = {
							"bridge_domain_id" : "",
							"vxrail_ae_interface" : parameters['vxrail_ae_interface'],
							"vxrail_logical_unit" : parameters['vxrail_logical_unit'],
							"sco_ae_interface" : parameters['sco_ae_interface'],
							"sco_logical_unit" : parameters['sco_logical_unit'],
							"public_cidr" : parameters['public_cidr']
						}

			self.path += "delete.conf"

		template = os.path.join(dir, self.path)

		return ("SUCCESS", template, jinja_vars)