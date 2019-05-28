import requests
import json
import os


def update_charles_service(service):
    url = os.getenv('CHARLES_URL') + 'services/'
    rheaders = {'Content-Type': 'application/json'}
    data = {'service_state': service.service_state}
    requests.post(url + service.service_id + "/process",
                  data=json.dumps(data),
                  verify=False,
                  headers=rheaders)
