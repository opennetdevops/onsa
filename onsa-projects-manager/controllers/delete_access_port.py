from flask import request, jsonify, Response
from flask_expects_json import expects_json

from settings import *
from models import *

@app.route('/api/projects/<string:id>/accessports/<string:port_id>', methods=['DELETE'])
def delete_access_port(id, port_id):
	project = Projects.objects(svc_id=id)[0]
	project.delete_access_port(port_id)
	return Response(status=200, mimetype='application/json')