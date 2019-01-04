from flask import request, jsonify, Response
from flask_expects_json import expects_json

from settings import *
from models import *

@app.route('/api/projects/<string:id>/vlans', methods=['GET'])
def get_project_vlans(id):
	project = Projects.objects(svc_id=id)[0]
	vlans = project.vlans
	response = [x.values() for x in vlans]

	return jsonify(response)