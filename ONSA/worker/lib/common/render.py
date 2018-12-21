import os
import ipaddress
import json

from pprint import pprint

from jinja2 import Environment, FileSystemLoader

def host(value):
    try:
        return list(ipaddress.ip_network(value).hosts())[0]
    except ValueError:
        print("not defined")
        return None
    

def second(value):
    try:
        return list(ipaddress.ip_network(value).hosts())[1]
    except ValueError:
        print("not defined")
        return None

def net(value):
    try:
        return ipaddress.ip_network(value)
    except ValueError:
        print("not defined")
        return None

def address(value):
    return ipaddress.ip_address(value)

def ip(value):
    return value.network_address

def prefix(value):
    if value is not None:    
        return value.prefixlen
    else:
        print("not defined")
        return None

def netmask(value):
    return value.netmask

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    env = Environment(loader=FileSystemLoader(path or './'))
    
    env.filters['net'] = net
    env.filters['ip'] = ip
    env.filters['host'] = host
    env.filters['netmask'] = netmask
    env.filters['prefix'] = prefix
    env.filters['address'] = address
    env.filters['second'] = second

    template = env.get_template(filename)

    # pprint(template.render(context)) 
    
    return template.render(context)