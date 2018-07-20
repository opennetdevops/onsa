import schedule
import time
import requests
import json

CORE_URL = "http://127.0.0.1:8000/core/api/services"
CHARLES_URL = "http://127.0.0.1:8000/charles/api/services"
# PENDING - REQUESTED - [COMPLETED / ERROR]

def check_core_services(state):
    #GET CORE SERVICES (pending)
    r = requests.get(CORE_URL + "?state=" + state)
    data = r.json()
    print(data)
    return data

def job():
    print("I'm working...")
    s = check_core_services("PENDING")

    for service in s:
        print(service['service_id'])
        print(service['status'])

        data = {
        "service_id":service['service_id'],
        "service_type":service['service_type'],
        "client_id":service['client_id'],
        "client_name":service['client_id'], #TODO CHANGE TO CLIENT NAME
        "location":"MOCK" #todo no need, charles will know this... eventually?
        }
        r = requests.post(CHARLES_URL + "", data = data)
        print("done")

def check_job():
    print("I'm checking work...")
    # s = check_core_services("REQUESTED")
    # #GET CHARLES SERVICES (REQUESTED)
    # for service in s:
    #     print(service)

    #FOR SERVICE IN CHARLES_SERVICES
    #    PUT CORE   

schedule.every(1).minutes.do(job)
schedule.every(1).minutes.do(check_job)

while True:
    schedule.run_pending()
    time.sleep(5)
