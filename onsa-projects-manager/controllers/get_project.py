from flask import request, jsonify, Response
from flask_expects_json import expects_json

from settings import *
from models import *

@app.route('/api/projects', methods=['GET'], defaults = {'id' : None})
@app.route('/api/projects/<string:id>', methods=['GET'])
def get_project(id):
	if id is None:
		projects = Projects.objects()
		response = []
		for project in projects:
			response.append(project.values())
		return jsonify(list(response))
	else:
		project = Project.objects(svc_id=id)[0]
		response = project.values()
		return jsonify(dict(response))