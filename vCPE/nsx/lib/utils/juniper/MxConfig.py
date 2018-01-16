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

def configure_bridge_domains(dev, bd_id, description, XXX, YYY):

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/bridge_domains.set')

	jinja_vars = {'id' : bd_id, 'description' : description, 'XXX' : XXX, 'YYY' : YYY}

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

def configure_interfaces(dev, XXX, YYY, ae1_description, ae2_description, vxrail_id, sco_id):

	logging.basicConfig(level=logging.INFO)

	dir = os.path.dirname(__file__)
	template_rac_file = os.path.join(dir, './templates/interfaces.set')

	jinja_vars = {'vxrail_id' : vxrail_id,
				  'sco_id' : sco_id,
				  'ae1_description' : ae1_description,
				  'ae2_description' : ae2_description,
				  'XXX' : XXX,
				  'YYY' : YYY}
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

def configure_static_route(dev, public_prefix, nexthop_vcpe):
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


def configure_vcpe_mx(user,
					  passwd,
					  host_rac,
					  bd_id,
					  description,
					  XXX,
					  YYY,
					  ae1_description,
					  ae2_description,
					  vxrail_id,
					  sco_id,
					  public_prefix,
					  nexthop_vcpe):

	logging.basicConfig(level=logging.INFO)

	dev = Device(host=host_rac, user=user, password=passwd, port=443)

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

	# configure_bridge_domains(dev, bd_id, description, XXX, YYY)
	# configure_interfaces(dev, XXX, YYY, ae1_description, ae2_description, vxrail_id, sco_id)
	configure_static_route(dev, public_prefix, nexthop_vcpe)
	commit_result = dev.cu.commit_check()
	logging.info("commit_result:")
	logging.info(commit_result)

	# logging.info( "Committing the configuration")
	# try:
	# 	# commit_result = dev.cu.commit()
	# 	# Show that the commit worked True means it worked, false means it failed
	# 	logging.debug( "Commit result: %s",commit_result)

	# except CommitError:
	# 	logging.error( "Error: Unable to commit configuration")
	# 	logging.error( "Unlocking the configuration")
	# 	try:
	# 		dev.cu.unlock()
	# 	except UnlockError:
	# 		logging.error( "Error: Unable to unlock configuration")
	# 		dev.close()
	# 		return

	logging.info( "Unlocking the configuration")
	try:
		 dev.cu.unlock()
	except UnlockError:
		 logging.error( "Error: Unable to unlock configuration")

	# End the NETCONF session and close the connection
	logging.info("Closing NETCONF session")
	dev.close()