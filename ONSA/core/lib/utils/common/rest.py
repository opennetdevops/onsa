import requests
import json

MANAGER = "http://10.120.78.90/"

def onsaGet(url):
  rheaders = {'Accept': 'application/json'}
  r = requests.get(MANAGER + url, auth = None, verify = False, headers = rheaders)
  return r.text

def onsaPost(url, data):
  rheaders = {'Content-Type': 'application/json'}
  r = requests.post(MANAGER + url, data = json.dumps(data), auth = None, verify = False, headers = rheaders)
  return r

def onsaDelete(url):
  rheaders = {'Content-Type': 'application/json'}
  r = requests.delete(MANAGER + url, auth = None, verify = False, headers = rheaders)
  return r