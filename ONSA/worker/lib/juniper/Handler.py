from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import jinja2
import logging, sys

from pprint import pprint

class Handler(object):

	@property
	def factory(service_type):
		if service_type == "MX_VCPE": return VcpeHandler()
		elif service_type == "MX_CPELESS": return CpelessHandler()

	def _open_conn():

		logging.basicConfig(level=logging.INFO)
		dev = Device(host=parameters["mgmt_ip"], user="lab", password="lab123", port=443)
		try:
			logging.info("Openning NETCONF connection to device")
			dev.open()
		except Exception as err:
			logging.error("Cannot connect to device:%s", err)
			status = False

		dev.bind(cu=Config)
		status = True
		
		return dev, status

	def _close_conn():
		# End the NETCONF session and close the connection
		logging.info("Closing NETCONF session")
		dev.close()
		return True

	def _lock_config(dev):

		# Lock the configuration
		logging.info("Locking the configuration")
		try:
			dev.cu.lock()
		except LockError:
			logging.error("Error: Unable to lock configuration")
			dev.close()
			status = False

		status = True

		return status

	def _unlock_config(dev):

		logging.info( "Unlocking the configuration")
		try:
			 dev.cu.unlock()
			 status = True
		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")
			 status = False

		return status

	def _load_config(dev, template, parameters):

		status = True

		# Loading configuration changes
		try:
			dev.cu.load(template_path=template, merge=True, template_vars=parameters, format="set")
			dev.cu.pdiff()

		except ValueError as err:
			logging.error("Error: %s", err.message)
			status = False

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
			status = False

		return status

	def _commit_config(dev):
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
				status = False
			except UnlockError:
				logging.error( "Error: Unable to unlock configuration")
				dev.close()
				status = False

		logging.info( "Unlocking the configuration")
		try:
			 dev.cu.unlock()
			 status = True
		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")
			 status = False

		return status

	def configure_mx(self, mx_parameters, method):

		status = True

		dev, outcome = Handler._open_conn()
		status &= outcome
		outcome = Handler._lock_config(dev)
		status &= outcome
		outcome, template_rac_file, parameters = Handler._generate_params(method, parameters)
		status &= outcome		
		outcome = Handler._load_config(dev, template_rac_file, parameters)
		status &= outcome
		outcome = Handler._unlock_config(dev)
		status &= outcome
		outcome = Handler._close_conn(dev)
		status &= outcome

		return status, parameters