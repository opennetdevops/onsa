import os
import ipaddress

from jinja2 import Environment, FileSystemLoader

def _host_query():
	pass

def ipaddr(value, query=''):

	query_func_map = {
						'address' : _ip_query,
						'host' : _host_query,
						'net' : _net_query
	}

	query = query_func_map[value]

	return query()


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    env = Environment(loader=FileSystemLoader(path or './'))

    template = env.get_template(filename)
    template.globals['ipaddr'] = ipaddr
    
    return template.render(context)