from django.db import models

from .lib.juniper.mx_config import *
from .lib.nsx.nsx_handler import NsxHandler
from enum import Enum


class Service(models.Model):
    service_id = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50) 

    def __str__(self):
        return self.service_id

    def create_task(self):
        task = Task(service=self)
        return task

    def delete_task(self):
        return access_nodes


class TaskChoices(Enum):
    MX_VCPE = "MX_VCPE"
    NSX_VCPE = "NSX_VCPE"
    NSX_MPLS = "NSX_MPLS"


class Task(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    task_state = models.CharField(default="Creating", max_length=50, blank=True)
    task_type = models.CharField(max_length=30)

    def __str__(self):
        return self.service.service_id

    def factory(model, service_type, service):
        if service_type == "vcpe":
            if model == "MX104": return MxVcpeTask(service=service, task_type=TaskChoices['MX_VCPE'].value)
            elif model == "NSX": return NsxTask(service=service, task_type=TaskChoices['NSX_VCPE'].value)
        elif service_type == "cpeless-irs":
            #todo change task type
            if model == "MX104": return MxCpelessIrsTask(service=service, task_type=TaskChoices['MX_VCPE'].value)


class MxVcpeTask(Task):

    class Meta:
        proxy = True
    
    def __str__(self):
        return self.service.service_id

    def run_task(self, device):
        handler = Handler.factory(service_type=self.task_type)
        handler.configure_mx(device['parameters'], "set")
        
        self.task_state = "success"
        return self.task_state

    def rollback(self, parameters):
        pass


class MxCpelessIrsTask(Task):

    class Meta:
        proxy = True
    
    def __str__(self):
        return self.service.service_id

    def run_task(self, parameters):
        handler = CpelessHandler("irs")
        handler.configure_mx(parameters, "set")
        self.task_state = "success"
        return self.task_state

    def rollback(self, parameters):
        pass


class NsxTask(Task):
    
    class Meta:
        proxy = True

    def __str__(self):
        return self.service.service_id

    def run_task(self,device):
        handler = NsxHandler()
        handler.create_edge(device['parameters'])
        # handler.add_gateway(parameters['name'])
        return self.task_state

    def rollback(self,parameters):
        pass

