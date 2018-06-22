#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from netaddr import *
import jinja2
import os
import argparse
import logging, sys

from pprint import pprint

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)

	return jinja2.Environment(
		loader=jinja2.FileSystemLoader(path or './')
	).get_template(filename).render(context)

class NsxHandler(object):
	def __init__(self):
		self.url = "./templates/nsxpublicirs/"

	def __set_interfaces(self, mx_parameters):

		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "set_interfaces.conf")

		jinja_vars = {
					  'vxrail_ae_interface' : mx_parameters['vxrail_ae_interface'],
					  'sco_ae_interface' : mx_parameters['sco_ae_interface'],
					  'vxrail_logical_unit' : mx_parameters['vxrail_logical_unit'],
					  'sco_logical_unit' : mx_parameters['sco_logical_unit'],
					  'description' : mx_parameters['service_description'],
					  'sco_outer_vlan' : mx_parameters['sco_outer_vlan'],
					  'vxrail_vlan' : mx_parameters['vxrail_vlan'],
					  'sco_inner_vlan' : mx_parameters['sco_inner_vlan'],
					  'public_network_ip' : mx_parameters['public_network_ip']
					  }

		pprint(jinja_vars)

		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			logging.error("Unable to load configuration changes: %s", err)
			logging.info("Unlocking the configuration")
			try:
				dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return


	def __delete_interfaces(self, dev, mx_parameters):

		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "delete_interfaces.conf")

		jinja_vars = {'vxrail_ae_interface' : mx_parameters['vxrail_ae_interface'],
					  'sco_ae_interface' : mx_parameters['sco_ae_interface'],
					  'vxrail_log_unit' : mx_parameters['vxrail_log_unit'],
					  'sco_logical_unit' : mx_parameters['sco_logical_unit'],
					  'vrf_name' : mx_parameters['vrf_name']}
		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				logging.error("Unable to load configuration changes: %s", rpc_msg)

			logging.info("Unlocking the configuration")
			try:
					dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return


	def __set_bridge_domains(self, dev, mx_parameters):

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "set_bridge_domains.conf")

		jinja_vars = 	{
							'id' : mx_parameters['client_id'], 
							'description' : mx_parameters['service_description'],
							'vxrail_ae_interface' : mx_parameters['vxrail_ae_interface'],
							'sco_ae_interface' : mx_parameters['sco_ae_interface'],
							'vxrail_log_unit' : mx_parameters['vxrail_logical_unit'],
							'sco_log_unit' : mx_parameters['sco_logical_unit'],
							'vlan_id' : mx_parameters['vlan_id']
						}

		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				logging.error("Unable to load configuration changes: %s", rpc_msg)

			logging.info("Unlocking the configuration")
			try:
					dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return

	def __set_static_route(self, dev, mx_parameters):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "set_static_route.conf")

		jinja_vars = {'public_prefix' : mx_parameters['public_prefix'],
					  'nexthop_vcpe': mx_parameters['nexthop_vcpe']}
		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				logging.error("Unable to load configuration changes: %s", rpc_msg)

			logging.info("Unlocking the configuration")
			try:
					dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return

	def __delete_bridge_domains(self, dev, mx_parameters):

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "delete_bridge_domains.conf")

		jinja_vars = {	'id' : mx_parameters['client_id'] }

		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				logging.error("Unable to load configuration changes: %s", rpc_msg)

			logging.info("Unlocking the configuration")
			try:
					dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return

	def __delete_static_route(self, dev, mx_parameters):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "delete_static_route.conf")

		jinja_vars = {'public_prefix' : mx_parameters['public_prefix']}

		try:
			logging.info("command: " + render(template_rac_file, jinja_vars))
			dev.cu.load(template_path=template_rac_file, replace=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			logging.error(err)

			logging.info("Unlocking the configuration")
			try:
				dev.cu.unlock()
			except UnlockError:
				logging.error("Error: Unable to unlock configuration")
			dev.close()
			return

	def configure_mx(self, mx_parameters, method):

		logging.basicConfig(level=logging.INFO)

		# 
		dev = Device(host=mx_parameters["mx_ip"], user="lab", password="lab123", port=443)

		try:
			logging.info("Openning NETCONF connection to device")
			dev.open()
		except Exception as err:
			logging.error("Cannot connect to device:%s", err)
			return

		dev.bind(cu=Config)

		# Lock the configuration, load configuration changes, and commit
		logging.info("Locking the configuration")
		try:
			dev.cu.lock()
		except LockError:
			logging.error("Error: Unable to lock configuration")
			dev.close()
			return

		if method == "set":
			logging.info("Setting bridge domains")
			__set_bridge_domains(dev, mx_parameters)

			logging.info("Setting interfaces")
			__set_interfaces(dev, mx_parameters)

			logging.info("Setting static route")
			__set_static_route(dev, mx_parameters)

		elif method == "delete":
			# logging.info("Deleting bridge domains")
			__delete_bridge_domains(dev, mx_parameters)

			logging.info("Deleting interfaces")
			__delete_interfaces(dev, mx_parameters)

			logging.info("Deleting static route")
			__delete_static_route(dev, mx_parameters)

		logging.info("Committing the configuration")
		try:
			dev.timeout=120
			commit_result = dev.cu.commit()
			# Show that the commit worked True means it worked, false means it failed
			logging.debug( "Commit result: %s",commit_result)

		except (CommitError, RpcTimeoutError) as e:
			logging.error( "Error: Unable to commit configuration")
			logging.error( "Unlocking the configuration")
			logging.error(e)
			try:
				dev.cu.unlock()
			except UnlockError:
				logging.error( "Error: Unable to unlock configuration")
				dev.close()
				return

		logging.info( "Unlocking the configuration")
		try:
			 dev.cu.unlock()
		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")

		# End the NETCONF session and close the connection
		logging.info("Closing NETCONF session")
		dev.close()

class CpelessHandler(object):
	def __init__(self, service):
		self.url = "./templates/cpeless/"+service

	def __set_interfaces(self, dev, mx_parameters):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "set_interfaces.conf")

		jinja_vars = {
					  'sco_ae_interface' : mx_parameters['sco_ae_interface'],
					  'sco_logical_unit' : mx_parameters['sco_logical_unit'],
					  'service_description' : mx_parameters['service_description'],
					  'sco_outer_vlan' : mx_parameters['sco_outer_vlan'],
					  'sco_inner_vlan' : mx_parameters['sco_inner_vlan'],
					  'public_network_ip' : mx_parameters['public_network_ip'],
					  'vrf_name' : mx_parameters["vrf_name"]
					  }

		pprint(jinja_vars)

		print(render(template_rac_file, jinja_vars))

		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			logging.error("Unable to load configuration changes: %s", err)
			logging.info("Unlocking the configuration")
			try:
				dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return


	def __delete_interfaces(self, dev, mx_parameters):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.url + "delete_interfaces.conf")

		jinja_vars = {
					  'sco_ae_interface' : mx_parameters['sco_ae_interface'],
					  'sco_logical_unit' : mx_parameters['sco_logical_unit'],
					  'vrf_name' : mx_parameters["vrf_name"]
					 }
		try:
			dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)

		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				logging.error("Unable to load configuration changes: %s", rpc_msg)

			logging.info("Unlocking the configuration")
			try:
					dev.cu.unlock()
			except UnlockError:
					logging.error("Error: Unable to unlock configuration")
			dev.close()
			return

	def configure_mx(self, mx_parameters, method):
		logging.basicConfig(level=logging.INFO)

		dev = Device(host=mx_parameters["mx_ip"], user="lab", password="lab123", port=443)

		try:
			logging.info("Openning NETCONF connection to device")
			dev.open()
		except Exception as err:
			logging.error("Cannot connect to device:%s", err)
			return

		dev.bind(cu=Config)

		# Lock the configuration, load configuration changes, and commit
		logging.info("Locking the configuration")
		try:
			dev.cu.lock()
		except LockError:
			logging.error("Error: Unable to lock configuration")
			dev.close()
			return

		if method == "set":
			logging.info("Setting interfaces")
			self.__set_interfaces(dev, mx_parameters)

		elif method == "delete":
			logging.info("Deleting interfaces")
			self.__delete_interfaces(dev, mx_parameters)

		logging.info("Committing the configuration")
		try:
			dev.timeout=120
			commit_result = dev.cu.commit()
			# Show that the commit worked True means it worked, false means it failed
			logging.debug( "Commit result: %s",commit_result)

		except (CommitError, RpcTimeoutError) as e:
			logging.error( "Error: Unable to commit configuration")
			logging.error( "Unlocking the configuration")
			logging.error(e)
			try:
				dev.cu.unlock()
			except UnlockError:
				logging.error( "Error: Unable to unlock configuration")
				dev.close()
				return

		logging.info( "Unlocking the configuration")
		try:
			 dev.cu.unlock()
		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")

		# End the NETCONF session and close the connection
		logging.info("Closing NETCONF session")
		dev.close()
