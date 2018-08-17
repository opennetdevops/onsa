from django.db import models
from django.contrib.postgres.fields import JSONField

import json
import time
import requests
import os

from enum import Enum
from background_task import background
from pprint import pprint

from .lib import ConfigHandler
from .lib.common.render import render

CHARLES = "http://localhost:8000"

class ServiceStates(Enum):
	IN_PROGRESS = "IN_PROGRESS"
	COMPLETED = "COMPLETED"
	ERROR = "ERROR"

class Service(models.Model):
	client_name = models.CharField(max_length=50)
	service_id = models.CharField(max_length=50)
	service_type = models.CharField(max_length=50)
	service_state = models.CharField(max_length=50)
	parameters = JSONField()

	def __str__(self):
		return self.service_id
		
	@background(schedule=5)
	def deploy(service_id):

		my_service = Service.objects.get(service_id=service_id)
		tasks = Task.objects.filter(service=my_service)

		print(tasks)

		executed_tasks = []

		my_service.service_state = "COMPLETED"

		for task in tasks:
			task.run_task()
			task.save()
			if task.task_state == "COMPLETED":
				executed_tasks.append(task)
			elif task.task_state == "ERROR":
				task.rollback()
				task.save()
				for task in executed_tasks:
					task.rollback()
					task.save()
				my_service.service_state = "ERROR"            
				break
		
		print(executed_tasks)
		my_service.save()

		"""
		Updates Charles' service status	
		"""
		rheaders = {'Content-Type': 'application/json'}
		data = {"service_state" : my_service.service_state}
		requests.put(CHARLES+"/charles/api/services/%s" % my_service.service_id, data = json.dumps(data), verify = False, headers = rheaders)


class TaskStates(Enum):
	IN_PROGRESS = "IN_PROGRESS"
	COMPLETED = "COMPLETED"
	ROLLBACKED = "ROLLBACKED"
	ERROR = "ERROR"

class OperationType(Enum):
	CREATE = "CREATE"
	UPDATE = "UPDATE"
	DELETE = "DELETE"

class Strategy(Enum):
	juniper = "pyez"
	vmware = "nsx"
	transition = "ssh"
	huawei = "netconf"
	cisco = "netconf"

class Task(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	task_state = models.CharField(max_length=50, blank=True)
	op_type = models.CharField(max_length=30)
	device = JSONField()

	def __str__(self):
		return self.service.service_id

	def run_task(self):
		dir = os.path.dirname(os.path.abspath(__file__))

		if self.device['vendor'] == 'transition':
			template_path = "templates/" + self.device['vendor'].lower() + "/" + self.device['model'].lower() + "/" + self.op_type.upper() + "_L2SERVICE.CONF"
		else:	
			template_path = "templates/" + self.device['vendor'].lower() + "/" + self.device['model'].lower() + "/" + self.op_type.upper() + \
				"_" + self.service.service_type.split("_")[1].upper() + self.service.service_type.split("_")[0].upper() + ".CONF"

		template_path = os.path.join(dir, template_path)

		variables_path = "variables/" + self.service.service_type.split("_")[1].upper() + self.service.service_type.split("_")[0].upper() + ".json"
		variables_path = os.path.join(dir, variables_path)

		pprint(template_path)
		pprint(variables_path)
		
		params = {}
		params['mgmt_ip'] = self.device['mgmt_ip']
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client_name'] = self.service.client_name

		params.update(self.service.parameters)

		# pprint(params)

		params = json.loads(render(variables_path, params))

		config_handler = getattr(ConfigHandler.ConfigHandler, Strategy[self.device['vendor']].value)

		status = config_handler(template_path, params)

		self.task_state = TaskStates['ERROR'].value if status is not True else TaskStates['COMPLETED'].value

		print(self.task_state)
			

	def rollback(self):

		print("DELETEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEe")

		dir = os.path.dirname(os.path.abspath(__file__))

		if self.device['vendor'] == 'transition':
			template_path = "templates/" + self.device['vendor'].lower() + "/" + self.device['model'].lower() + "/" + "DELETE_L2SERVICE.CONF"
		else:	
			template_path = "templates/" + self.device['vendor'].lower() + "/" + self.device['model'].lower() + "/" + "DELETE_" + self.service.service_type.split("_")[1].upper() + self.service.service_type.split("_")[0].upper() + ".CONF"

		template_path = os.path.join(dir, template_path)

		variables_path = "variables/" + self.service.service_type.split("_")[1].upper() + self.service.service_type.split("_")[0].upper() + ".json"
		variables_path = os.path.join(dir, variables_path)

		pprint(template_path)
		pprint(variables_path)
		
		params = {}
		params['mgmt_ip'] = self.device['mgmt_ip']
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client_name'] = self.service.client_name

		params.update(self.service.parameters)

		params = json.loads(render(variables_path, params))

		config_handler = getattr(ConfigHandler.ConfigHandler, Strategy[self.device['vendor']].value)

		status = config_handler(template_path, params)

		self.task_state = TaskStates['ERROR'].value if status is not True else TaskStates['ROLLBACKED'].value

		print(self.task_state)