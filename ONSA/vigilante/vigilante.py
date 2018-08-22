import schedule
import time
import requests
import json

from pprint import pprint

CORE_URL = "http://127.0.0.1:8000/core/api/pending_services"
CORE_CLIENT_URL = "http://127.0.0.1:8000/core/api/clients"
CHARLES_URL = "http://127.0.0.1:8000/charles/api/services"

rheaders = {'Content-Type': 'application/json'}

# PENDING - REQUESTED - [COMPLETED / ERROR]


def check_url_services(url,state):
	r = requests.get(CORE_URL + "?state=" + state)
	data = r.json()    
	return data

def job():
	# print("I'm working...")
	s = check_url_services(CORE_URL,"PENDING")

	for service in s:
		#GET CLIENT Name
		r = requests.get(CORE_CLIENT_URL + "/" + str(service['client_id']) )
		clientData = r.json()

		data = { 'data_model' : {
									"service_id" : service['service_id'],
									"service_type" : service['service_type'],
									"client_id" : service['client_id'],
									"client_name" : clientData[0]['name'],
									"location": "LAB" #todo no need, charles will know this... eventually?
								},
				"prefix" : service['prefix'],
				"client_node_port" : service['client_node_port'],
				"client_node_sn" : service['client_node_sn'],
				"bandwidth" : service['bandwidth']
		}

		pprint(data)

		r = requests.post(CHARLES_URL, data = json.dumps(data), headers=rheaders)
		#if 200 --> PUT core to change service state to REQUESTED
		if r.ok:
			data = {
			"service_state":"REQUESTED"
			}
		else:
			data = {
			"service_state":"ERROR"
			}
		r = requests.put(CORE_URL + "/" + str(service['service_id']), data = json.dumps(data), headers=rheaders)


def check_job():
	# print("I'm checking work...")
	s = check_url_services(CORE_URL,"REQUESTED")

	for service in s:
		# print(service)
		r = requests.get(CHARLES_URL + "/" + str(service['service_id']))
		data = r.json()
		if not data['service_state'] == "REQUESTED":
			newdata = {
			"service_state":data['service_state']
			}
			p = requests.put(CORE_URL + "/" + str(service['service_id']), data = json.dumps(newdata), headers=rheaders)



schedule.every(20).seconds.do(job)
schedule.every(40).seconds.do(check_job)

while True:
	schedule.run_pending()
	time.sleep(5)
