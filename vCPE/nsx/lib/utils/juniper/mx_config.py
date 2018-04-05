#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from netaddr import *
import jinja2
import os
import argparse
import logging, sys


# host = '10.120.78.204'
# host  = 10.106.16.104
# user = aliguori
# passwd = Anabel15

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)

	return jinja2.Environment(
		loader=jinja2.FileSystemLoader(path or './')
	).get_template(filename).render(context)

def set_bridge_domains(dev,
	client_id,
	service_description,
	vxrail_ae_interface,
	sco_ae_interface,
	vxrail_log_unit,
	sco_log_unit):


	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/bridge_domains.set')

	jinja_vars = {	'id' : client_id, 
					'description' : service_description,
					'vxrail_ae_interface' : vxrail_ae_interface,
					'sco_ae_interface' : sco_ae_interface,
					'vxrail_log_unit' : vxrail_log_unit,
					'sco_log_unit' : sco_log_unit}

	try:
		dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars)
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

def set_interfaces(dev, vxrail_ae_interface, sco_ae_interface, vxrail_log_unit, 
						service_description, sco_log_unit, sco_outer_vlan,
						vxrail_vlan, sco_inner_vlan):

	logging.basicConfig(level=logging.INFO)

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/interfaces.set')

	jinja_vars = {'vxrail_ae_interface' : vxrail_ae_interface,
				  'sco_ae_interface' : sco_ae_interface,
				  'vxrail_log_unit' : vxrail_log_unit,
				  'sco_log_unit' : sco_log_unit,
				  'description' : service_description,
				  'sco_outer_vlan' : sco_outer_vlan,
				  'vxrail_vlan' : vxrail_vlan,
				  'sco_inner_vlan' : sco_inner_vlan
				  }
	try:
		dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars)
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

def set_static_route(dev, public_prefix, nexthop_vcpe):
	logging.basicConfig(level=logging.INFO)

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/static_route.set')

	jinja_vars = {'public_prefix' : public_prefix,
				  'nexthop_vcpe': nexthop_vcpe}
	try:
		dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars)
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


def delete_bridge_domains(dev,
						  client_id,
						  service_description,
						  vxrail_ae_interface,
						  sco_ae_interface,
						  vxrail_log_unit,
						  sco_log_unit):

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/bridge_domains.delete')

	jinja_vars = {	'id' : client_id, 
					'description' : service_description,
					'vxrail_ae_interface' : vxrail_ae_interface,
					'sco_ae_interface' : sco_ae_interface,
					'vxrail_log_unit' : vxrail_log_unit,
					'sco_log_unit' : sco_log_unit}

	try:
		dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars)
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

def delete_interfaces(dev,
					  vxrail_ae_interface,
					  sco_ae_interface,
					  vxrail_log_unit,
					  service_description,
					  sco_log_unit,
					  sco_outer_vlan,
					  vxrail_vlan,
					  sco_inner_vlan):

	logging.basicConfig(level=logging.INFO)

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/interfaces.delete')

	jinja_vars = {'vxrail_ae_interface' : vxrail_ae_interface,
				  'sco_ae_interface' : sco_ae_interface,
				  'vxrail_log_unit' : vxrail_log_unit,
				  'sco_log_unit' : sco_log_unit,
				  'description' : service_description,
				  'sco_outer_vlan' : sco_outer_vlan,
				  'vxrail_vlan' : vxrail_vlan,
				  'sco_inner_vlan' : sco_inner_vlan
				  }
	try:
		dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars)
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

def delete_static_route(dev, public_prefix, nexthop_vcpe):
	logging.basicConfig(level=logging.INFO)

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/static_route.delete')

	jinja_vars = {'public_prefix' : public_prefix,
				  'nexthop_vcpe': nexthop_vcpe}
	try:
		dev.cu.load(template_path=template_rac_file, merge=True, template_vars=jinja_vars)
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



def configure_mx(mx_parameters, method):

	logging.basicConfig(level=logging.INFO)

	# 
	dev = Device(host=mx_parameters["mx_ip"], user=mx_parameters["username"], password=mx_parameters["password"], port=443 )

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
		# logging.info("Setting bridge domains")
		set_bridge_domains(dev,
							mx_parameters["client_id"],
							mx_parameters["service_description"],
							mx_parameters["vxrail_ae_interface"],
							mx_parameters["sco_ae_interface"],
							mx_parameters["vxrail_logical_unit"],
							mx_parameters["sco_logical_unit"])

		# logging.info("Setting interfaces")
		set_interfaces(dev,
						mx_parameters["vxrail_ae_interface"],
						mx_parameters["sco_ae_interface"],
						mx_parameters["vxrail_logical_unit"],
						mx_parameters["service_description"],
						mx_parameters["sco_logical_unit"],
						mx_parameters["sco_outer_vlan"],
						mx_parameters["vxrail_vlan"],
						mx_parameters["sco_inner_vlan"])

		logging.info("Setting static route")
		set_static_route(dev, mx_parameters["public_network_ip"], mx_parameters["ip_wan"])

	elif method == "delete":
		# logging.info("Deleting bridge domains")
		delete_bridge_domains(dev,
								mx_parameters["client_id"],
								mx_parameters["service_description"],
								mx_parameters["vxrail_ae_interface"],
								mx_parameters["sco_ae_interface"],
								mx_parameters["vxrail_logical_unit"],
								mx_parameters["sco_logical_unit"])

		# logging.info("Deleting interfaces")
		delete_interfaces(dev,
							mx_parameters["vxrail_ae_interface"],
							mx_parameters["sco_ae_interface"],
							mx_parameters["vxrail_logical_unit"],
							mx_parameters["service_description"],
							mx_parameters["sco_logical_unit"],
							mx_parameters["sco_outer_vlan"],
							mx_parameters["vxrail_vlan"],
							mx_parameters["sco_inner_vlan"])

		logging.info("Deleting static route")
		delete_static_route(dev, mx_parameters["public_network_ip"], mx_parameters["ip_wan"])

	

	logging.info("Committing the configuration")
	try:
		dev.timeout=120
		commit_result = dev.cu.commit_check()
		# Show that the commit worked True means it worked, false means it failed
		logging.debug( "Commit result: %s",commit_result)

	except (CommitError, RpcTimeoutError) as e:
		logging.error( "Error: Unable to commit configuration")
		logging.error( "Unlocking the configuration")
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