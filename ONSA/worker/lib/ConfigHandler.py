from netmiko import ConnectHandler
from jinja2 import Template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import ipaddress
import requests

def get_edge_id_by_name(name):
	rheaders = {'Accept': 'application/json'}

	r = requests.get(MANAGER + "/api/4.0/edges", auth=(USER, PASS), verify=False, headers=rheaders)

	r_dict = json.loads(r.text)	
	allEdges = r_dict['edgePage']['data']

	for edge in allEdges:
		if edge['name'] == name:
			return edge['id']

	return ""


class ConfigHandler:
	def pyez(parameters, template_path):

		logging.basicConfig(level=logging.INFO)
		dev = Device(host=mgmt_ip, user="lab", password="lab123", port=443)
		dev.bind(cu=Config)

		try:
			logging.info("Openning NETCONF connection to device")
			dev.open()
		except Exception as err:
			logging.error("Cannot connect to device:%s", err)


		logging.info("Locking the configuration")
		try:
			dev.cu.lock()
		except LockError:
			logging.error("Error: Unable to lock configuration")
			dev.close()

		try:
			dev.cu.load(template_path=template_path, merge=True, template_vars=parameters, format="set")
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

		logging.info("Committing the configuration")
		try:
			dev.timeout=120
			commit_result = dev.cu.commit()
			# Show that the commit worked True means it worked, false means it failed
			logging.debug( "Commit result: %s",commit_result)
		except (CommitError, RpcTimeoutError) as e:
			logging.error( "Error: Unable to commit configuration")
			dev.cu.unlock()
			dev.cu.close()

		logging.info( "Unlocking the configuration")
		try:
			 dev.cu.unlock()
		except UnlockError:
			 logging.error( "Error: Unable to unlock configuration")

		logging.info("Closing NETCONF session")
		dev.close()


	def transition(parameters, template_path):
		my_device = {
		'host': parameters['mgmt_ip'],
		'username': "lab",
		'password': "lab123",
		'device_type': 'cisco_ios',
		'global_delay_factor': 1
		}

		params['port_description'] = params['client'] + "-" + params['service_type'] + "-" + params['service_id']

		dir = os.path.dirname(__file__)
		path = os.path.join(dir, template_path)

		lines = open(path,'r').read().splitlines()

		config = []

		for line in lines:
			template = Template(line)
			config.append(template.render(**params))

		net_connect = ConnectHandler(**my_device)
		output = net_connect.send_config_set(config)

		print(output)
		
		# Clossing connection    
		net_connect.disconnect()

	def nsx(parameters, template_path):
		dir = os.path.dirname(__file__)
		nsx_edge_xml = os.path.join(dir, template_path)

		params = {'create_params' : parameters['create_params']}

		data = render(nsx_edge_xml, params)

		rheaders = {'Content-Type': 'application/xml'}
		r = requests.post(MANAGER + "/api/4.0/edges", data=data, auth=(USER, PASS), verify=False, headers=rheaders)

		sleep(45)

		edge_id = get_edge_id_by_name(parameters['create_params']['name'])
		nsx_static_json = os.path.join(dir, template_path)

		params = {'gateway_params' : parameters['gateway_params']}

		data = render(nsx_static_json, params) 

		rheaders = {'Content-Type': 'application/json'}
		r = requests.put(MANAGER + "/api/4.0/edges/%s/routing/config/static" % edge_id, data=data, auth=(USER, PASS), verify=False, headers=rheaders)
		status_code = r.status_code