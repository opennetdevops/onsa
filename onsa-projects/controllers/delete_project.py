from flask import request, jsonify, Response
from flask_expects_json import expects_json

from models import *
from settings import *

@app.route('/api/projects/<string:id>', methods=['DELETE'])
def delete_project(id):
	project = Projects.objects(svc_id=id)[0]
	project.delete()

	return Response(status=200, mimetype='application/json')