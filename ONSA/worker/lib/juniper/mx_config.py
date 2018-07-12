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

class Handler(object):

	@staticmethod
	def factory(service_type):
		if service_type == "vcpe": return VcpeHandler()
		elif service_type == "cpeless": return CpelessHandler()

	def _set_interfaces(self, parameters, dev=None):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.path+"set/set_interfaces.conf")

		print(render(template_rac_file,parameters))

		# try:
		# 	dev.cu.load(template_path=template_rac_file, merge=True, template_vars=parameters, format="set")
		# 	dev.cu.pdiff()

		# except ValueError as err:
		# 	logging.error("Error: %s", err.message)

		# except Exception as err:
		# 	logging.error("Unable to load configuration changes: %s", err)
		# 	logging.info("Unlocking the configuration")
		# 	try:
		# 		dev.cu.unlock()
		# 	except UnlockError:
		# 			logging.error("Error: Unable to unlock configuration")
		# 	dev.close()
		# 	return

	def _delete_interfaces(self, parameters, dev=None):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.path+"delete/delete_interfaces.conf")

		print(render(template_rac_file, parameters))

		# try:
		# 	dev.cu.load(template_path=template_rac_file, merge=True, template_vars=parameters, format="set")
		# 	dev.cu.pdiff()

		# except ValueError as err:
		# 	logging.error("Error: %s", err.message)

		# except Exception as err:
		# 	if err.rsp.find('.//ok') is None:
		# 		rpc_msg = err.rsp.findtext('.//error-message')
		# 		logging.error("Unable to load configuration changes: %s", rpc_msg)

		# 	logging.info("Unlocking the configuration")
		# 	try:
		# 			dev.cu.unlock()
		# 	except UnlockError:
		# 			logging.error("Error: Unable to unlock configuration")
		# 	dev.close()
		# 	return

	def _set_static_route(self, parameters, dev=None):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.path+"set/set_static_route.conf")

		print(render(template_rac_file, parameters))

		# try:
		# 	dev.cu.load(template_path=template_rac_file, merge=True, template_vars=parameters, format="set")
		# 	dev.cu.pdiff()

		# except ValueError as err:
		# 	logging.error("Error: %s", err.message)

		# except Exception as err:
		# 	if err.rsp.find('.//ok') is None:
		# 		rpc_msg = err.rsp.findtext('.//error-message')
		# 		logging.error("Unable to load configuration changes: %s", rpc_msg)

		# 	logging.info("Unlocking the configuration")
		# 	try:
		# 			dev.cu.unlock()
		# 	except UnlockError:
		# 			logging.error("Error: Unable to unlock configuration")
		# 	dev.close()
		# 	return

	def _delete_static_route(self, parameters,  dev=None):
		logging.basicConfig(level=logging.INFO)

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.path + "/delete/delete_static_route.conf")

		print(render(template_rac_file, parameters))

		# try:
		# 	logging.info("command: " + render(template_rac_file, jinja_vars))
		# 	dev.cu.load(template_path=template_rac_file, replace=True, template_vars=parameters, format="set")
		# 	dev.cu.pdiff()

		# except ValueError as err:
		# 	logging.error("Error: %s", err.message)

		# except Exception as err:
		# 	logging.error(err)

		# 	logging.info("Unlocking the configuration")
		# 	try:
		# 		dev.cu.unlock()
		# 	except UnlockError:
		# 		logging.error("Error: Unable to unlock configuration")
		# 	dev.close()
		# 	return

class VcpeHandler(Handler):
	def __init__(self):
		self.path = "../../templates/mx104/vcpe/"

	def _set_bridge_domains(self, parameters, dev=None):

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.path+"set/set_bridge_domains.conf")

		print(render(template_rac_file, parameters))

		# try:
		# 	dev.cu.load(template_path=template_rac_file, merge=True, template_vars=parameters, format="set")
		# 	dev.cu.pdiff()

		# except ValueError as err:
		# 	logging.error("Error: %s", err.message)

		# except Exception as err:
		# 	if err.rsp.find('.//ok') is None:
		# 		rpc_msg = err.rsp.findtext('.//error-message')
		# 		logging.error("Unable to load configuration changes: %s", rpc_msg)

		# 	logging.info("Unlocking the configuration")
		# 	try:
		# 			dev.cu.unlock()
		# 	except UnlockError:
		# 			logging.error("Error: Unable to unlock configuration")
		# 	dev.close()
		# 	return

	def _delete_bridge_domains(self, parameters, dev=None):

		dir = os.path.dirname(__file__)
		template_rac_file = os.path.join(dir, self.path+"delete/delete_bridge_domains.conf")

		print(render(template_rac_file, parameters))

		# try:
		# 	dev.cu.load(template_path=template_rac_file, merge=True, template_vars=parameters, format="set")
		# 	dev.cu.pdiff()

		# except ValueError as err:
		# 	logging.error("Error: %s", err.message)

		# except Exception as err:
		# 	if err.rsp.find('.//ok') is None:
		# 		rpc_msg = err.rsp.findtext('.//error-message')
		# 		logging.error("Unable to load configuration changes: %s", rpc_msg)

		# 	logging.info("Unlocking the configuration")
		# 	try:
		# 			dev.cu.unlock()
		# 	except UnlockError:
		# 			logging.error("Error: Unable to unlock configuration")
		# 	dev.close()
		# 	return

	def configure_mx(self, parameters, method):

		# logging.basicConfig(level=logging.INFO)

		# # 
		# dev = Device(host=mx_parameters["mgmt_ip"], user="lab", password="lab123", port=443)

		# try:
		# 	logging.info("Openning NETCONF connection to device")
		# 	dev.open()
		# except Exception as err:
		# 	logging.error("Cannot connect to device:%s", err)
		# 	return

		# dev.bind(cu=Config)

		# # Lock the configuration, load configuration changes, and commit
		# logging.info("Locking the configuration")
		# try:
		# 	dev.cu.lock()
		# except LockError:
		# 	logging.error("Error: Unable to lock configuration")
		# 	dev.close()
		# 	return

		if method == "set":
			# logging.info("Setting bridge domains")
			VcpeHandler._set_bridge_domains(self, parameters['bridge_domains'])

			# logging.info("Setting interfaces")
			VcpeHandler._set_interfaces(self, parameters['interfaces'])

			# logging.info("Setting static route")
			VcpeHandler._set_static_route(self, parameters['routes'])

		elif method == "delete":
			# logging.info("Deleting bridge domains")
			VcpeHandler._delete_bridge_domains(self, parameters['bridge_domains'])

			# logging.info("Deleting interfaces")
			VcpeHandler._delete_interfaces(self, parameters['interfaces'])

			# logging.info("Deleting static route")
			VcpeHandler._delete_static_route(self, parameters['routes'])

		# logging.info("Committing the configuration")
		# try:
		# 	dev.timeout=120
		# 	commit_result = dev.cu.commit()
		# 	# Show that the commit worked True means it worked, false means it failed
		# 	logging.debug( "Commit result: %s",commit_result)

		# except (CommitError, RpcTimeoutError) as e:
		# 	logging.error( "Error: Unable to commit configuration")
		# 	logging.error( "Unlocking the configuration")
		# 	logging.error(e)
		# 	try:
		# 		dev.cu.unlock()
		# 	except UnlockError:
		# 		logging.error( "Error: Unable to unlock configuration")
		# 		dev.close()
		# 		return

		# logging.info( "Unlocking the configuration")
		# try:
		# 	 dev.cu.unlock()
		# except UnlockError:
		# 	 logging.error( "Error: Unable to unlock configuration")

		# # End the NETCONF session and close the connection
		# logging.info("Closing NETCONF session")
		# dev.close()

class CpelessHandler(object):
	def __init__(self, service):
		self.path = "../templates/mx104/"+service

	def configure_mx(self, mx_parameters, method):
		# logging.basicConfig(level=logging.INFO)

		# dev = Device(host=mx_parameters["mx_ip"], user="lab", password="lab123", port=443)

		# try:
		# 	logging.info("Openning NETCONF connection to device")
		# 	dev.open()
		# except Exception as err:
		# 	logging.error("Cannot connect to device:%s", err)
		# 	return

		# dev.bind(cu=Config)

		# # Lock the configuration, load configuration changes, and commit
		# logging.info("Locking the configuration")
		# try:
		# 	dev.cu.lock()
		# except LockError:
		# 	logging.error("Error: Unable to lock configuration")
		# 	dev.close()
		# 	return

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
