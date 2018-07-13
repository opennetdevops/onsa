from django.db import models

from .lib.juniper.mx_config import *
from .lib.nsx.edge import *
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


class Task(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    task_state = models.CharField(default="Creating", max_length=50, blank=True)

    task_type = models.CharField(max_length=20)

    def __str__(self):
        return self.service.service_id

    def factory(model, service_type, service):
        if service_type == "vcpe":
            print(TaskChoices.MX_VCPE)
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

    def run_task(self, parameters, task_type):
        if task_type == "CREATE" or task_type == "UPDATE":
            handler = Handler.factory(service_type="vcpe")
            handler.configure_mx(parameters, "set")
        elif task_type == "DELETE":
            handler = Handler.factory(service_type="vcpe")
            handler.configure_mx(parameters, "delete")

        self.task_state = "Completed"
        return self.task_state

    def rollback(self, parameters):
        handler = Handler.factory(service_type="vcpe")
        handler.configure_mx(parameters, "delete")
        return self.task_state


class MxCpelessIrsTask(Task):

    class Meta:
        proxy = True
    
    def __str__(self):
        return self.service.service_id

    def run_task(self, parameters):
        handler = CpelessHandler("irs")
        handler.configure_mx(parameters, "set")
        self.task_state = "Completed"
        return self.task_state

    def rollback(self, parameters):
        return self.task_state


class NsxTask(Task):
    
    class Meta:
        proxy = True

    def __str__(self):
        return self.service.service_id

    def run_task(self, parameters, service_type):
        pprint(parameters)
        # nsx_edge_create(parameters)
        # edge_id = nsx_edge_get_id_by_name(parameters['name'])
        # nsx_edge_add_gateway(edge_id, "0", "100.64.4.1", "1500")
        return self.task_state

    def rollback(self, parameters):
        return self.task_state

