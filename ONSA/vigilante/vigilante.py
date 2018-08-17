import schedule
import time
import requests
import json

CORE_URL = "http://127.0.0.1:8000/core/api/pending_services"
CORE_CLIENT_URL = "http://127.0.0.1:8000/core/api/clients"
CHARLES_URL = "http://127.0.0.1:8000/charles/api/services"

rheaders = {'Content-Type': 'application/json'}

# PENDING - REQUESTED - [COMPLETED / ERROR]


def check_url_services(url,state):
    r = requests.get(CORE_URL + "?state=" + state)
    data = r.json()
    # print(data)
    return data

def job():
    # print("I'm working...")
    s = check_url_services(CORE_URL,"PENDING")

    for service in s:
        #GET CLIENT Name
        r = requests.get(CORE_CLIENT_URL + "/" + str(service['client_id']) )
        clientData = r.json()

        data = {
        "service_id":service['service_id'],
        "service_state":"PENDING",
        "service_type":service['service_type'],
        "client_id":service['client_id'],
        "client_name":clientData[0]['name'],
        "prefix": service['public_prefix'],
        "location":"LAB" #todo no need, charles will know this... eventually?
        }
        # print("DEBUG: ",data)

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
        r = requests.put(CORE_URL + "/" + service['service_id'], data = json.dumps(data), headers=rheaders)


def check_job():
    # print("I'm checking work...")
    s = check_url_services(CORE_URL,"REQUESTED")

    for service in s:
        # print(service)
        r = requests.get(CHARLES_URL + "/" + service['service_id'])
        data = r.json()
        if not data['service_state'] == "REQUESTED":
            newdata = {
            "service_state":data['service_state']
            }
            p = requests.put(CORE_URL + "/" + service['service_id'], data = json.dumps(newdata), headers=rheaders)



schedule.every(20).seconds.do(job)
schedule.every(40).seconds.do(check_job)

while True:
    schedule.run_pending()
    time.sleep(5)
