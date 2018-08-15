import os
import ipaddress
import json

from jinja2 import Environment, FileSystemLoader

def host(value):
	return list(ipaddress.ip_network(value).hosts())[0]

def net(value):
	return ipaddress.ip_network(value)

def ip(value):
	value = value.split("/")[0]
	return ipaddress.ip_address(value)

def netmask(value):
	return value.netmask

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)
	env = Environment(loader=FileSystemLoader(path or './'))
	
	env.filters['net'] = net
	env.filters['ip'] = ip
	env.filters['host'] = host
	env.filters['netmask'] = netmask

	template = env.get_template(filename) 
	
	return template.render(context)