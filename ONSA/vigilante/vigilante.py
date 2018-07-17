import schedule
import time
import requests
import json

CORE_URL = "http://127.0.0.1/core/api/services"
CHARLES_URL = "http://127.0.0.1/charles/api/services"
# PENDING - REQUESTED - [COMPLETED / ERROR]

def job():
    print("I'm working...")
    #GET CORE SERVICES (pending)
    r = requests.get(CORE_URL)
    data = r.json()
    print(data)

    #FOR SERVICE IN CORE_SERVICES
    #    POST CHARLES
    data = {
    "client":"Starbucks",
    "service_type":"vcpe",
    "service_id":"0987654321",
    "tasks_type":""
    }

    # r = requests.post(CHARLES_URL + "/", data = {'key':'value'})

def check_job():
    print("I'm checking work...")
    #GET CHARLES SERVICES (IN_PROGRESS)

    #FOR SERVICE IN CHARLES_SERVICES
    #    PUT CORE   

schedule.every(1).minutes.do(job)
schedule.every(1).minutes.do(check_job)

while True:
    schedule.run_pending()
    time.sleep(5)
