import requests

def get(url, format):
  rheaders = {'Accept': 'application/%s' % format}
  r = requests.get(MANAGER + url, auth = None, verify = False, headers = rheaders)
  return r.text


def post(url, data, format):
  rheaders = {'Content-Type': 'application/%s' % format}
  r = requests.post(MANAGER + url, data = data, auth = None, verify = False, headers = rheaders)
  return r