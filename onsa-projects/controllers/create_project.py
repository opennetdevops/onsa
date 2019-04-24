from flask import request, jsonify, Response
from flask_expects_json import expects_json

from settings import *
from models import *
from schemas import *

@app.route('/api/projects', methods=['POST'])
@expects_json(json_post_schema)
def create_project():
    data = request.json
    project = Projects(svc_id=data['svc_id'], bandwidth=data['bandwidth'])	
    if 'access_ports' in data.keys():
        access_ports = data['access_ports']
        project.add_access_ports(access_ports)	
    if 'vlans' in data.keys():
        vlans = data['vlans']
        project.add_vlans(vlans)	
    if 'locations' in data.keys():
        locs = data['locations']
        project.add_locations(locs)	
    if 'vrfs' in data.keys():
        vrfs = data['vrfs']
        project.add_vrfs(vrfs)  
    project.save()  
    return Response(status=201, mimetype='application/json')

