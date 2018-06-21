import json
from pprint import pprint


pg_list = []

idx = 3502

for i in range(0,400):
	pg_list.append({"fields" : {"vlan-tag" : "%d" % idx, "hub" : "1", "used" : False, "name" : "PG-CEN-VLAN%d" % idx}, "model" : "nsx.portgroup", "pk" : "%d" % (i+1)})
	idx += 1

with open('pg_fixtures.json', 'w') as outfile:
	json.dump(pg_list, outfile)






	
