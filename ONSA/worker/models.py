from django.db import models
from django.contrib.postgres.fields import JSONField

from .lib.juniper.Handler import Handler
from .lib.nsx.NsxHandler import NsxHandler
from enum import Enum

from background_task import background

from itertools import chain
import requests

import json


CHARLES = "http://localhost:8000"

class ServiceStates(Enum):
	IN_PROGRESS = "IN_PROGRESS"
	COMPLETED = "COMPLETED"
	ERROR = "ERROR"


class Service(models.Model):
	
	service_id = models.CharField(max_length=50)
	service_type = models.CharField(max_length=50)
	service_state = models.CharField(max_length=50)

	def __str__(self):
		return self.service_id
		
	@background(schedule=5)
	def deploy(service_id):
		my_service = Service.objects.get(service_id=service_id)
		tasks = list(chain(NsxTask.objects.filter(service=my_service), MxVcpeTask.objects.filter(service=my_service)))

		my_service.service_state = "COMPLETED"

		executed_tasks = []

		print(tasks)
		
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

		my_service.save()

		"""
		Updates Charles' service status	
		"""

		USER = "admin"
		PASS = "F1b3rc0rp!"
		rheaders = {'Content-Type': 'application/json'}
		data = {"service_state" : my_service.service_state}
		requests.put(CHARLES+"/api/charles/services/%s" % my_service.service_id, data = json.dumps(data), auth = (USER, PASS), verify = False, headers = rheaders)



class TaskStates(Enum):
	IN_PROGRESS = "IN_PROGRESS"
	COMPLETED = "COMPLETED"
	ROLLBACKED = "ROLLBACKED"
	ERROR = "ERROR"


class TaskChoices(Enum):
	MX_VCPE = "MX_VCPE"
	NSX_VCPE = "NSX_VCPE"
	NSX_MPLS = "NSX_MPLS"


class Task(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	task_state = models.CharField(default="Creating", max_length=50, blank=True)
	task_type = models.CharField(max_length=30)
	config = JSONField()


	def __str__(self):
		return self.service.service_id

	def factory(model, service_type, service, config):
		if service_type == "vcpe":
			if model == "MX104":
				return MxVcpeTask(service=service, task_state=TaskStates['IN_PROGRESS'],task_type=TaskChoices['MX_VCPE'].value, config=config)
			elif model == "NSX":
				return NsxTask(service=service, task_state=TaskStates['IN_PROGRESS'], task_type=TaskChoices['NSX_VCPE'].value, config=config)
		elif service_type == "cpeless-irs":
			#todo change task type
			if model == "MX104": return MxCpelessIrsTask(service=service, task_state=TaskStates['IN_PROGRESS'], task_type=TaskChoices['MX_VCPE'].value, config=config)

class ManagerTaskMx(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskMx, self).get_queryset().filter(
			task_type=TaskChoices['MX_VCPE'].value)


class ManagerTaskNsx(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskNsx, self).get_queryset().filter(
			task_type=TaskChoices['NSX_VCPE'].value)

class MxVcpeTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskMx()

	def run_task(self):
		handler = Handler.factory(service_type=self.task_type)
		status, configuration = handler.configure_mx(self.confg, "set")

		if status is not True:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['COMPLETED'].value
			self.config = configuration

	def rollback(self):
		handler = Handler.factory(service_type=self.task_type)
		if handler.configure_mx(self.config, "delete") is True:
			self.task_state = TaskStates['ROLLBACKED'].value

class MxCpelessIrsTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskMx()

	def run_task(self):
		handler = CpelessHandler("irs")
		status, configuration = handler.configure_mx(self.config, "set")
		if status is not True:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['COMPLETED'].value
			self.config = configuration

	def rollback(self):
		handler = CpelessHandler("irs")

		status, configuration = handler.configure_mx(self.config, "delete")
		if status is True:
			self.task_state = TaskStates['ROLLBACKED'].value

class NsxTask(Task):
	
	class Meta:
		proxy = True

	objects = ManagerTaskNsx()

	def get_queryset(self):
		return super(NsxTask, self).get_queryset().filter(
			task_type=TaskChoices['NSX_VCPE'].value)


	def run_task(self):
		handler = NsxHandler()

		status_code, create_edge_config =  handler.create_edge(self.config)
		if status_code != 204:
			self.task_state = TaskStates['ERROR'].value
			return
		status_code, add_gateway_config = handler.add_gateway("VCPE-Test")
		if status_code != 201:
			self.task_state = TaskStates['ERROR'].value
			return

		configuration = {'create_edge_config' : create_edge_config,
						'add_gateway_config' : add_gateway_config}

		self.config = configuration
		self.task_state = TaskStates['COMPLETED'].value

	def rollback(self):
		handler = NsxHandler()
		status_code = handler.delete_edge("VCPE-Test")
		self.task_state = TaskStates['ROLLBACKED'].value

		if status_code is not 200:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['ROLLBACKED'].value