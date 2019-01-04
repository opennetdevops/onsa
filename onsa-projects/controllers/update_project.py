
from flask import request, jsonify, Response
from flask_expects_json import expects_json

from settings import *
from models import *
from schemas import *

@app.route('/api/projects/<string:id>', methods=['PUT'])
@expects_json(json_put_schema)
def update_project(id):
	data = request.json

	project = Project.objects(svc_id=id)[0]
	project.update(**data)
	project.save()
	response = project.values()

	return jsonify(response)
