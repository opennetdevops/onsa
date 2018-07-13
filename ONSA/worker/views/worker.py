from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from pprint import pprint

from ..models import Service, Task


import json
from transitions import Machine

from ..lib.juniper.mx_config import *
from ..lib.nsx.edge import *

class TaskMachine(object):
	def __init__(self):
		self.task_state = False

	def run_task(self, task, parameters): 
		self.task_state = task.run_task(parameters['parameters'], parameters['tasks_type'])

	def rollback(self, task, parameters):
		pass

class WorkerView(View):
	def get(self, request):
		data = {"message" : "test"}
		return JsonResponse(data, safe=False)

	def post(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		service = Service(service_id=data['service_id'], service_type=data['service_type'], service_state="Requested")
		service.save()

		states = ['init', 'mx', 'nsx', 'access', 'rollback', 'end']

		transitions = [
			{ 'trigger': 'init', 'source' : 'init', 'dest' : 'mx'},
		    { 'trigger': 'success', 'source': 'mx', 'dest': 'nsx'},
		    { 'trigger': 'success', 'source': 'nsx', 'dest': 'access'},
		    { 'trigger': 'success', 'source': 'access', 'dest': 'end'},
		    { 'trigger': 'failed', 'source': 'mx', 'dest': 'rollback'},
		    { 'trigger': 'failed', 'source': 'nsx', 'dest': 'rollback'},
		    { 'trigger': 'failed', 'source': 'access', 'dest': 'rollback'}
		]

		taskMachine = TaskMachine()
		machine = Machine(taskMachine, states=states, transitions=transitions, initial='init')
		machine.on_enter_mx('run_task')
		machine.on_enter_nsx('run_task')
		machine.on_enter_access('run_task')
		machine.on_enter_rollback('rollback')

		taskMachine.init(task=task, parameters=parameters)
		
		while taskMachine.success:
			taskMachine.success(task=task)

		if ~taskMachine.success: taskMachine.failed()


	

		response = {"message" : "created"}
		return JsonResponse(response)

	def put(self, request):
		data = json.loads(request.body.decode(encoding='UTF-8'))

		data = serializers.serialize('json',)
		return HttpResponse(data, content_type='application/json')

	def delete(self, request):		
		data = '{"Message" : "Logical Unit deleted successfully"}'
		return HttpResponse(data, content_type='application/json')