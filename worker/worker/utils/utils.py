import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('conf/worker.conf')

def update_charles_service(service):
	rheaders = {'Content-Type': 'application/json'}
	data = {'service_state' : service.service_state}
	requests.post(config['urls']['charles'] + '/services/' + service.service_id + "/process",
				  data=json.dumps(data),
				  verify=False,
				  headers=rheaders)
