## BORRAR ##

from jinja2 import Template
from netmiko import ConnectHandler

config = []

lines = open('set.conf','r').read().splitlines()

params = {"service_vlan" : "3499",
			 "client" : "Starbucks",
			 "client_port" : "5",
			 "port_description" : "Starbucks-IRS"}

for line in lines:
	template = Template(line)
	config.append(template.render(**params))

my_device = {
	'host': "10.120.80.56",
	'username': "lab",
	'password': "lab123",
	'device_type': 'cisco_ios',
	'global_delay_factor': 1,
}

net_connect = ConnectHandler(**my_device)

output = net_connect.send_config_set(config)

print(output)


