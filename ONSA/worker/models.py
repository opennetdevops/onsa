from django.db import models
from django.contrib.postgres.fields import JSONField

from .lib.juniper.Handler import Handler
from .lib.nsx.NsxHandler import NsxHandler
from .lib.transition.TransitionHandler import TransitionHandler
from enum import Enum

from background_task import background

from itertools import chain
import requests
from pprint import pprint
import json
import time

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

	def __str__(self):
		return self.service_id
		
	@background(schedule=5)
	def deploy(service_id):

		my_service = Service.objects.get(service_id=service_id)

		print(my_service.service_id)

		if my_service.service_type.split("_")[0] == "vcpe":
			tasks = list(chain(MxVcpeTask.objects.filter(service=my_service),
							   NsxTask.objects.filter(service=my_service),
							   ScoTransitionTask.objects.filter(service=my_service),
							   NidTransitionTask.objects.filter(service=my_service)))
		elif my_service.service_type.split("_")[0] == "cpeless":
			tasks = list(chain(MxCpelessTask.objects.filter(service=my_service),
							   ScoTransitionTask.objects.filter(service=my_service),
							   NidTransitionTask.objects.filter(service=my_service)))
		elif my_service.service_type.split("_")[0] == "cpe":
			tasks = list(chain(MxCpeTask.objects.filter(service=my_service),
							   ScoTransitionTask.objects.filter(service=my_service),
							   NidTransitionTask.objects.filter(service=my_service)))

		print(tasks)

		executed_tasks = []

		my_service.service_state = "COMPLETED"

		for task in tasks:
			print(task.task_type)
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
	model = models.CharField(max_length=30)
	params = JSONField()

	def __str__(self):
		return self.service.service_id

	def factory(model, op_type, service_type, service, parameters):

		print(service_type)

		if service_type.split("_")[0] == "vcpe":
			if model.lower() == "mx104":
				return MxVcpeTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value,task_type=TaskChoices['MX_VCPE'].value, op_type=op_type, params=parameters)
			elif model.lower() == "nsx":
				return NsxTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value, task_type=TaskChoices['NSX_VCPE'].value, op_type=op_type, params=parameters)
			elif model.lower() == "s4224":
				return ScoTransitionTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value, task_type=TaskChoices['SCO'].value, op_type=op_type, params=parameters)
			elif model.lower() == "s3290-5":
				return NidTransitionTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value, task_type=TaskChoices['NID'].value, op_type=op_type, params=parameters)
		elif service_type.split("_")[0] == "cpeless":
			if model.lower() == "mx104":
				return MxCpelessTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value, task_type=TaskChoices['MX_CPELESS'].value, op_type=op_type,  params=parameters)
			elif model.lower() == "s4224":
				return ScoTransitionTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value, task_type=TaskChoices['SCO'].value, op_type=op_type, params=parameters)
			elif model.lower() == "s3290-5":
				return NidTransitionTask(service=service, model=model, task_state=TaskStates['IN_PROGRESS'].value, task_type=TaskChoices['NID'].value, op_type=op_type, params=parameters)

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
		return super(ManagerTaskCpeless, self).get_queryset().filter(
			task_type=TaskChoices['MX_CPELESS'].value)

class ManagerTaskSco(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskSco, self).get_queryset().filter(
			task_type=TaskChoices['SCO'].value)

class ManagerTaskNid(models.Manager):
	def get_queryset(self):
		return super(ManagerTaskNid, self).get_queryset().filter(
			task_type=TaskChoices['NID'].value)

class ManagerRouterNodeTask(models.Manager):
	def get_queryset(self):
		return super(ManagerRouterNodeTask, self).get_queryset().filter(
			task_type=TaskChoices['RouterNode'].value)

class ManagerAccessNodeTask(models.Manager):
	def get_queryset(self):
		return super(ManagerAccessNodeTask, self).get_queryset().filter(
			task_type=TaskChoices['AccessNode'].value)

class ManagerOpticalNodeTask(models.Manager):
	def get_queryset(self):
		return super(ManagerOpticalNodeTask, self).get_queryset().filter(
			task_type=TaskChoices['OpticalNode'].value)

class ManagerClientNodeTask(models.Manager):
	def get_queryset(self):
		return super(ManagerClientNodeTask, self).get_queryset().filter(
			task_type=TaskChoices['ClientNode'].value)



class MxVcpeTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskMx()

	def run_task(self):
		handler = Handler.factory(service_type=self.service.service_type)

		params = self.params
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client_name'] = self.service.client_name

		status = handler.configure_mx(params, "set")[0]

		if status is not True:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['COMPLETED'].value

	def rollback(self):
		handler = Handler.factory(service_type=self.service.service_type)
		
		params = self.params
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client_name'] = self.service.client_name

		if handler.configure_mx(params, "delete") is True:
			self.task_state = TaskStates['ROLLBACKED'].value

class MxCpelessTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskCpeless()

	def run_task(self):
		handler = Handler.factory(service_type=self.service.service_type)

		params = self.params
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client_name'] = self.service.client_name

		status = handler.configure_mx(params, "set")[0]

		if status is not True:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['COMPLETED'].value

	def rollback(self):
		handler = Handler.factory(service_type=self.service.service_type)
		
		params = self.params
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client_name'] = self.service.client_name

		if handler.configure_mx(params, "delete") is True:
			self.task_state = TaskStates['ROLLBACKED'].value

class NsxTask(Task):
	
	class Meta:
		proxy = True

	objects = ManagerTaskNsx()

	def run_task(self):
		handler = NsxHandler()
		
		self.task_state = TaskStates['COMPLETED'].value

		params = self.params
		edge_name = self.service.client_name+"-"+self.service.service_id
		"""
		Creates NSX Edge
		"""
		status_code, create_edge_config =  handler.create_edge(params, edge_name=edge_name)

		print(status_code)

		if status_code != 201:
			self.task_state = TaskStates['ERROR'].value

		time.sleep(45)

		# """
		# Add gateway to NSX Edge
		# """
		status_code, add_gateway_config = handler.add_gateway(edge_name)

		print(status_code)

		if status_code != 204:
			self.task_state = TaskStates['ERROR'].value

		parameters = {'create_edge_config' : create_edge_config,
						'add_gateway_config' : add_gateway_config}

		self.params = parameters


	def rollback(self):
		handler = NsxHandler()

		edge_name = self.service.client_name+"-"+self.service.service_id

		status_code = handler.delete_edge(edge_name)
		
		if status_code is not 200:
			self.task_state = TaskStates['ERROR'].value
		else:
			self.task_state = TaskStates['ROLLBACKED'].value


class ScoTransitionTask(Task):
	
	class Meta:
		proxy = True

	objects = ManagerTaskSco()

	def run_task(self):

		params = self.params
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client'] = self.service.client_name

		handler = TransitionHandler(params['mgmt_ip'])
		status = handler.configure_tn("set", self.model, params)

		if status is True:
			self.task_state = TaskStates['COMPLETED'].value
			self.params = params
		else:
			self.task_state = TaskStates['ERROR'].value

	def rollback(self):
		handler = TransitionHandler(self.params['mgmt_ip'])
		handler.configure_tn("delete", self.model, self.params)


class NidTransitionTask(Task):

	class Meta:
		proxy = True

	objects = ManagerTaskNid()

	def run_task(self):

		params = self.params
		params['service_id'] = self.service.service_id
		params['service_type'] = self.service.service_type
		params['client'] = self.service.client_name

		handler = TransitionHandler(self.params['mgmt_ip'])
		status = handler.configure_tn("set", self.model, params)

		if status is True:
			self.task_state = TaskStates['COMPLETED'].value
			self.params = params
		else:
			self.task_state = TaskStates['ERROR'].value


	def rollback(self):
		handler = TransitionHandler(self.params['mgmt_ip'])
		handler.configure_tn("delete", self.model, self.params)