from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import jinja2
import logging, sys, os

from pprint import pprint

from ..common.render import render

class Handler(object):

	def factory(service_type):
		if service_type == "vcpe_irs":
			return VcpeHandler(service_type)
		elif service_type == "cpeless_irs" or service_type == "cpeless_mpls": 
			return CpelessHandler(service_type)
		elif service_type == "cpe_irs" or service_type == "cpe_mpls":
			return CpeHandler(service_type)

	def _open_conn(self, mgmt_ip):

		logging.basicConfig(level=logging.INFO)
		dev = Device(host=mgmt_ip, user="lab", password="lab123", port=443)



		try:
			logging.info("Openning NETCONF connection to device")
			dev.open()

		except Exception as err:
			logging.error("Cannot connect to device:%s", err)
			status = False



		dev.bind(cu=Config)
		status = True
		
		return dev, status

	def _close_conn(self, dev):
		# End the NETCONF session and close the connection
		logging.info("Closing NETCONF session")
		


		dev.close()
		return True

	def _lock_config(self, dev):

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

	def _unlock_config(sefl, dev):
		status = False

		logging.info( "Unlocking the configuration")

		try:
			 dev.cu.unlock()
			 status = True

		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")


		return status

	def _load_config(self, dev, template, parameters):

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

	def _commit_config(self, dev):
		logging.info("Committing the configuration")

		status = False
		
		try:
			dev.timeout=120
			commit_result = dev.cu.commit()
			# Show that the commit worked True means it worked, false means it failed
			logging.debug( "Commit result: %s",commit_result)
			status = True

		except (CommitError, RpcTimeoutError) as e:
			logging.error( "Error: Unable to commit configuration")

		return status

	def _rollback_config(self, dev):
		try:
			print ("Rolling back the configuration")
			dev.cu.rollback(rb_id=0)
			print ("Committing the configuration")
			return True
		except RpcError as err:
		   print ("Unable to rollback configuration changes: {0}".format(err))
		   return False

	
	def rollback_mx(self, dev):
		status = True

		dev, outcome = Handler._open_conn()
		status &= outcome
		outcome = self._lock_config(dev)
		status &= outcome
		outcome = self._rollback_config(dev)
		status &= outcome		
		outcome = self._commit_config(dev)
		status &= outcome
		outcome = self._unlock_config(dev)
		status &= outcome
		outcome = self._close_conn(dev)
		status &= outcome

		return status, parameters

	def configure_mx(self, mx_parameters, method):

		print("************")
		print(method.upper())

		status = True

		dev, outcome = self._open_conn(mx_parameters['mgmt_ip'])
		status &= bool(outcome)
		print(status)
		outcome = self._lock_config(dev)
		status &= bool(outcome)
		print(status)

		outcome, template_rac_file, parameters = self._generate_params(method, mx_parameters)
		status &= bool(outcome)
		print(status)		
		outcome = self._load_config(dev, template_rac_file, parameters)
		status &= bool(outcome)
		print(status)
		outcome = self._commit_config(dev)
		status &= bool(outcome)
		print(status)
		outcome = self._unlock_config(dev)
		status &= bool(outcome)
		print(status)
		outcome = self._close_conn(dev)
		status &= bool(outcome)

		print(status)



		return bool(status), parameters


class VcpeHandler(Handler):
	def __init__(self, service_type):
		self.path = "../../templates/juniper/mx104/vcpe/%s/" % service_type.split("_")[1]

	def _generate_params(self, method, parameters):
		dir = os.path.dirname(__file__)

		bridge_domain_id = parameters['service_type'] + "-" + parameters['client_name']+ "-" + parameters["service_id"]

		if method == "set":			
			jinja_vars = {
							"bridge_domain_id" : bridge_domain_id,
							"bridge_domain_description" : "asdsadsa",
							"vmw_uplinkInterface" : parameters['vmw_uplinkInterface'],
							"vmw_logicalUnit" : parameters['vmw_logicalUnit'],
							"an_uplinkInterface" : parameters['an_uplinkInterface'],
							"an_logicalUnit" : parameters['an_logicalUnit'],
							"vmw_interface_description" : "",
							"an_interface_description" : "",
							"vmw_vlan" : parameters['vmw_vlan'],
							"an_qinqOuterVlan" : parameters['an_qinqOuterVlan'],
							"an_qinqInnerVlan" : parameters['an_qinqInnerVlan'],
							"public_cidr" : parameters['public_cidr']
						}
			
			self.path += "set.conf"

		elif method == "delete":

			jinja_vars = {
							"bridge_domain_id" : bridge_domain_id,
							"vmw_uplinkInterface" : parameters['vmw_uplinkInterface'],
							"vmw_logicalUnit" : parameters['vmw_logicalUnit'],
							"an_uplinkInterface" : parameters['an_uplinkInterface'],
							"an_logicalUnit" : parameters['an_logicalUnit'],
							"public_cidr" : parameters['public_cidr']
						}

			self.path += "delete.conf"

		template = os.path.join(dir, self.path)

		return ("SUCCESS", template, jinja_vars)


class CpelessHandler(Handler):
	def __init__(self, service_type):
		self.path = "../../templates/juniper/mx104/cpeless/%s/" % service_type.split("_")[1]

	def _generate_params(self, method, parameters):
		dir = os.path.dirname(__file__)
		if method == "set":			
			jinja_vars = {
							"an_uplinkInterface" : parameters['an_uplinkInterface'],
							"an_logicalUnit" : parameters['an_logicalUnit'],
							"sco_interface_description" : "",
							"vrf_name" : parameters["vrf_name"],
							"an_qinqOuterVlan" : parameters['an_qinqOuterVlan'],
							"an_qinqInnerVlan" : parameters['an_qinqInnerVlan'],
							"public_cidr" : parameters['public_cidr']
						}
			
			self.path += "set.conf"

		elif method == "delete":

			jinja_vars = {
							"an_uplinkInterface" : parameters['an_uplinkInterface'],
							"an_logicalUnit" : parameters['an_logicalUnit'],
							"vrf_name" : parameters["vrf_name"]
						}

			self.path += "delete.conf"

		template = os.path.join(dir, self.path)

		return "SUCCESS", template, jinja_vars

class CpeHandler(Handler):
	def __init__(self, service_type):
		self.path = "../../templates/juniper/mx104/cpe/%s/" % service_type.split("_")[1]
		
	def _generate_params(self, method, parameters):
		dir = os.path.dirname(__file__)
		if method == "set":			
			jinja_vars = {}
			
			self.path += "set.conf"

		elif method == "delete":
			jinja_vars = {}

			self.path += "delete.conf"

		template = os.path.join(dir, self.path)

		return "SUCCESS", template, jinja_vars