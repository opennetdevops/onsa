from flask import request, jsonify, Response
from flask_expects_json import expects_json

from settings import *
from models import *

@app.route('/api/projects/<string:id>/locations/<string:loc_id>/logicalunits/<string:lu_id>', methods=['DELETE'])
def delete_lu_in_loc(id, loc_id, lu_id):
	project = Projects.objects(svc_id=id)[0]
	project.delete_logical_unit(loc_id, lu_id)
	return Response(status=200, mimetype='application/json')