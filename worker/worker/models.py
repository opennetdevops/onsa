# Django imports
from django.db import models
from django.contrib.postgres.fields import JSONField

# Python imports
import json
import time
import requests
import os
from enum import Enum
from pprint import pprint


# ONSA imports
from worker.lib import ConfigHandler
from worker.lib.common.render import render
from worker.utils.worker_maps import *
from worker.utils.utils import *


class Service(models.Model):
    client_name = models.CharField(max_length=50)
    service_id = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50)
    parameters = JSONField()

    def __str__(self):
        return self.service_id

    def deploy(self):
        tasks = Task.objects.filter(service=self)

        print("Service Id: ", self.service_id)
        print("Requested Tasks: ", tasks)

        completed_tasks = []
        failed_tasks = []

        self.service_state = "ERROR"

        for task in tasks:
            task.run_task()
            task.save()
            if task.task_state == "ERROR":
                completed_tasks.append(task)
            elif task.task_state != "ERROR":
                task.rollback()
                task.save()
                failed_tasks.append(task)
                self.service_state = task.task_state
                break

        print("Completed Tasks: ", completed_tasks)
        print("Failed Tasks: ", failed_tasks)
        self.save()

        # Let charles know about service state
        update_charles_service(self)


class Task(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    task_state = models.CharField(max_length=50, blank=True)
    op_type = models.CharField(max_length=30)
    device = JSONField()

    def __str__(self):
        return self.service.service_id

    def _gen_template_path(self):
        if self.device['vendor'] == 'transition':
            template_path = "templates/" + self.device['vendor'].lower(
            ) + "/" + self.device['model'].lower() + "/" + self.op_type.upper() + "_L2SERVICE.CONF"
        else:
            if self.service.service_type != "vpls":
                template_path = "templates/" + VendorMap[self.device['vendor']].lower() + "/" + self.device['model'].lower() + "/" + self.op_type.upper() + \
                    "_" + self.service.service_type.split("_")[1].upper(
                ) + self.service.service_type.split("_")[0].upper() + ".CONF"
            else:
                template_path = "templates/" + VendorMap[self.device['vendor']].lower() + "/" + self.device['model'].lower() + "/" + self.op_type.upper() + \
                    "_" + self.service.service_type.upper() + ".CONF"

        return template_path

    def run_task(self):
        dir = os.path.dirname(os.path.abspath(__file__))

        # Generates template path
        template_path = self._gen_template_path()
        template_path = os.path.join(dir, template_path)
        pprint(template_path)

        # Generates variables path
        variables_path = "variables/" + self.service.service_type.upper() + ".json"
        variables_path = os.path.join(dir, variables_path)
        pprint(variables_path)

        # Set up parameters
        params = {}
        params['mgmt_ip'] = self.device['mgmt_ip']
        params['service_id'] = self.service.service_id
        params['service_type'] = self.service.service_type
        params['client_name'] = self.service.client_name

        params.update(self.service.parameters)

        params = json.loads(render(variables_path, params))

        config_handler = getattr(
            ConfigHandler.ConfigHandler, StrategyMap[VendorMap[self.device['vendor']]])

        status = config_handler(template_path, params)

        if (status == ERR0):
            self.task_state = status
        else:
            self.task_state = status

        print(self.task_state)

    def rollback(self):

        dir = os.path.dirname(os.path.abspath(__file__))

        if self.device['vendor'] == 'transition':
            template_path = "templates/" + VendorMap[self.device['vendor']].lower() + "/" + self.device['model'].lower() + "/" + "DELETE_L2SERVICE.CONF"
        else:
            if self.service.service_type != "vpls":
                template_path = "templates/" + VendorMap[self.device['vendor']].lower() + "/" + self.device['model'].lower(
                ) + "/" + "DELETE_" + self.service.service_type.split("_")[1].upper() + self.service.service_type.split("_")[0].upper() + ".CONF"
            else:
                template_path = "templates/" + VendorMap[self.device['vendor']].lower() + "/" + self.device['model'].lower(
                ) + "/" + "DELETE_" + self.service.service_type.upper() + ".CONF"

        template_path = os.path.join(dir, template_path)

        variables_path = "variables/" + self.service.service_type.upper() + ".json"
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

        config_handler = getattr(
            ConfigHandler.ConfigHandler, StrategyMap[VendorMap[self.device['vendor']]])

        status = config_handler(template_path, params)

        self.task_state = 'NO_ROLLBACK' if status is not True else 'ROLLBACK'

        print(self.task_state)
