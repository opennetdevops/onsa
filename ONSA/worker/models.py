from django.db import models
from django.contrib.postgres.fields import JSONField

from .lib.juniper.mx_config import *
from .lib.nsx.nsx_handler import NsxHandler
from enum import Enum

from background_task import background

from itertools import chain

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
			task_state = task.run_task()
			if task_state == "success":
				executed_tasks.append(task)
			elif task_state == "failed":
			# 	# task.rollback()
			# 	# for task in executed_tasks:
			# 	# 	task_state = task.rollback()
				my_service.service_state = "ERROR"            
				break

		print(executed_tasks)

		my_service.save()


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
				return MxVcpeTask(service=service, task_type=TaskChoices['MX_VCPE'].value, config=config)
			elif model == "NSX":
				return NsxTask(service=service, task_type=TaskChoices['NSX_VCPE'].value, config=config)
		elif service_type == "cpeless-irs":
			#todo change task type
			if model == "MX104": return MxCpelessIrsTask(service=service, task_type=TaskChoices['MX_VCPE'].value, config=config)

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
		self.task_state = handler.configure_mx(self.config, "set")
		return self.task_state

	def rollback(self, parameters):
		handler = Handler.factory(service_type=self.task_type)
		pass


class MxCpelessIrsTask(Task):

	class Meta:
		proxy = True

	def run_task(self):
		handler = CpelessHandler("irs")
		self.task_state = handler.configure_mx(self.config, "set")
		return self.task_state

	def rollback(self, parameters):
		pass


class NsxTask(Task):
	
	class Meta:
		proxy = True

	objects = ManagerTaskNsx()

	def get_queryset(self):
		return super(NsxTask, self).get_queryset().filter(
			task_type=TaskChoices['NSX_VCPE'].value)


	def run_task(self):
		handler = NsxHandler()
		self.task_state = handler.create_edge(self.config)
		self.task_state =  handler.add_gateway(parameters['name'])
		return self.task_state

	def rollback(self,parameters):
		pass

