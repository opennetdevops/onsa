from django.core import serializers
from django.http import HttpResponse
from django.views import View

from pprint import pprint
from ..lib.juniper.mx_config import *
from ..lib.nsx.edge import *

import json


class WorkerView(View):
	def get(self, request):
		data = '{"message" : "test"}'
		return HttpResponse(data, content_type='application/json')

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		if data['service'] == "vcpe-irs":
			if data['model'] == "MX104":
				handler = NsxHandler()
				handler.configure_mx(data, "set")
			elif data['model'] == "NSX":
				nsx_edge_create(data)
				edge_id = nsx_edge_get_id_by_name(data['name'])
				nsx_edge_add_gateway(edge_id, "0", "100.64.4.1", "1500")
		elif data['service'] == "cpeless-irs":
			if data['model'] == "MX104":
				handler = CpelessHandler("irs")
				handler.configure_mx(data, "set")	

		response = '{"message" : "created"}'
		return HttpResponse(response, content_type='application/json')

	def put(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		data = serializers.serialize('json',)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request):		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')