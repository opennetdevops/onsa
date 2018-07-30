from django.db import models
from django.contrib.postgres.fields import JSONField

from .lib.juniper.Handler import Handler
from .lib.nsx.NsxHandler import NsxHandler
from .lib.transition.TransitionHandler import TransitionHandler
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

		if service_type.split("_")[0] == "vcpe":
			tasks = list(chain(NsxTask.objects.filter(service=my_service), MxVcpeTask.objects.filter(service=my_service)))
		elif service_type.split("_")[0] == "cpeless":
			tasks = list(chain(MxVcpeTask.objects.filter(service=my_service)))
		elif service_type.split("_")[0] == "cpe":
			tasks = list(chain(MxVcpeTask.objects.filter(service=my_service)))

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
		
		my_service.save()

		"""
		Updates Charles' service status	
		"""
		rheaders = {'Content-Type': 'application/json'}
		data = {"service_state" : my_service.service_state}
		requests.put(CHARLES+"/api/charles/services/%s" % my_service.service_id, data = json.dumps(data), verify = False, headers = rheaders)



class TaskStates(Enum):
	IN_PROGRESS = "IN_PROGRESS"
	COMPLETED = "COMPLETED"
	ROLLBACKED = "ROLLBACKED"
	ERROR = "ERROR"


class TaskChoices(Enum):
	MX_VCPE = "MX_VCPE"
	MX_CPELESS = "MX_CPELESS"
	NSX_VCPE = "NSX_VCPE"
	NSX_MPLS = "NSX_MPLS"
	SCO = "SCO"
	NID = "NID"


class Task(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	task_state = models.CharField(default="Creating", max_length=50, blank=True)
	task_type = models.CharField(max_length=30)
	op_type = models.CharField(max_length=30)
	params = JSONField()


	def __str__(self):
		return self.service.service_id

	def factory(model, op_type, service_type, service, parameters):
		if service_type.split("_")[0] == "vcpe":
			if model.lower() == "mx104":
				return MxVcpeTask(service=service, task_state=TaskStates['IN_PROGRESS'],task_type=TaskChoices['MX_VCPE'].value, op_type=op_type, params=parameters)
			elif model.lower() == "nsx":
				return NsxTask(service=service, task_state=TaskStates['IN_PROGRESS'], task_type=TaskChoices['NSX_VCPE'].value, op_type=op_type, params=parameters)
			elif model.lower() == "s4224":
				return ScoTransitionTask(service=service, task_state=TaskStates['IN_PROGRESS'], task_type=TaskChoices['SCO'].value, op_type=op_type, params=parameters)
			elif model.lower() == "s3290-5":
				return ScoTransitionTask(service=service, task_state=TaskStates['IN_PROGRESS'], task_type=TaskChoices['SCO'].value, op_type=op_type, params=parameters)

		elif service_type.split("_")[0] == "cpeless":
			if model.lower() == "mx104" and service_type.split("_")[1] == "irs":
				return MxCpelessIrsTask(service=service, task_state=TaskStates['IN_PROGRESS'], task_type=TaskChoices['MX_CPELESS'].value, op_type=op_type,  params=parameters)

class ManagerTaskMx(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskMx, self).get_queryset().filter(
			task_type=TaskChoices['MX_VCPE'].value)

class ManagerTaskNsx(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskNsx, self).get_queryset().filter(
			task_type=TaskChoices['NSX_VCPE'].value)

class ManagerTaskCpeless(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskNsx, self).get_queryset().filter(
			task_type=TaskChoices['MX_CPELESS'].value)

class ManagerTaskSco(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskNsx, self).get_queryset().filter(
			task_type=TaskChoices['SCO'].value)

class ManagerTaskNid(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskNsx, self).get_queryset().filter(
			task_type=TaskChoices['NID'].value)

class MxVcpeTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskMx()

	def run_task(self):
		handler = Handler.factory(service_type=self.service.service_type)
		status, parameters = handler.configure_mx(self.params, "set")

		if status is not True:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['COMPLETED'].value
			self.params = params

	def rollback(self):
		handler = Handler.factory(service_type=self.task_type)
		if handler.configure_mx(self.params, "delete") is True:
			self.task_state = TaskStates['ROLLBACKED'].value

class MxCpelessIrsTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskCpeless()

	def run_task(self):
		handler = Handler.factory(service_type=self.service.service_type)
		status, parameters = handler.configure_mx(self.params, "set")
		if status is not True:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['COMPLETED'].value
			self.params = parameters

	def rollback(self):
		handler = CpelessHandler("irs")

		status, parameters = handler.configure_mx(self.params, "delete")
		if status is True:
			self.task_state = TaskStates['ROLLBACKED'].value

class NsxTask(Task):
	
	class Meta:
		proxy = True

	objects = ManagerTaskNsx()

	def run_task(self):
		handler = NsxHandler()

		status_code, create_edge_config =  handler.create_edge(self.params)
		if status_code != 204:
			self.task_state = TaskStates['ERROR'].value
			return
		status_code, add_gateway_config = handler.add_gateway("VCPE-Test")
		if status_code != 201:
			self.task_state = TaskStates['ERROR'].value
			return

		configuration = {'create_edge_config' : create_edge_config,
						'add_gateway_config' : add_gateway_config}

		self.params = parameters
		self.task_state = TaskStates['COMPLETED'].value

	def rollback(self):
		handler = NsxHandler()
		status_code = handler.delete_edge("VCPE-Test")
		self.task_state = TaskStates['ROLLBACKED'].value

		if status_code is not 200:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['ROLLBACKED'].value


class ScoTransitionTask(Task):
	
	class Meta:
		proxy = True

	objects = ManagerTaskSco()


	def run_task(self):
		handler = TransitionHandler(self.params['mgmt_ip'], self.params['model'])
		handler.configure_tn()


	def rollback(self):
		handler = TransitionHandler(self.params['mgmt_ip'], self.params['model'])
				handler.configure_tn()


class NidTransitionTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskNid()

	def run_task(self):
		handler = TransitionHandler(self.params['mgmt_ip'], self.params['model'])
		handler.configure_tn()


	def rollback(self):
		handler = TransitionHandler(self.params['mgmt_ip'], self.params['model'])
		handler.configure_tn()