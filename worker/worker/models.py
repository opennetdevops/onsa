# Django imports
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

# Python imports
import json
import time
import requests
import os
from enum import Enum
from pprint import pprint
import logging


# ONSA imports
from worker.lib import ConfigHandler
from worker.lib.common.render import render
from worker.utils.worker_maps import *
from worker.utils.utils import *
from worker.constants import *
from worker.exceptions import *


class Service(models.Model):
    client_name = models.CharField(max_length=50)
    service_id = models.CharField(max_length=50, primary_key=True)
    service_type = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50)
    parameters = JSONField()

    def __str__(self):
        return self.service_id

    def deploy(self):
        tasks = Task.objects.filter(
            service=self, task_state=INITIAL_TASK_STATE)

        # print("Service Id: ", self.service_id)
        # print("Requested Tasks: ", tasks)

        completed_tasks = []
        failed_tasks = []

        self.service_state = CONFIG_GENERAL_ERROR

        for task in tasks:
            task.run_task()
            task.save()
            if  task.task_state not in ERROR_STATES:
                completed_tasks.append(task)
            elif task.task_state in ROLLBACK_STATES:
                task.rollback()
                task.save()
                failed_tasks.append(task)
                # TODO DO FOR completed tasks rollback
                # for t in completed_tasks:
                #     t.rollback()
                #     t.save()
                break
            else:
                self.service_state = task.task_state
                # do not rollback, since this failed task is not "rollbackeable"

        if len(failed_tasks):
            self.service_state = CONFIG_GENERAL_ERROR
        elif len(completed_tasks) == len(tasks):
            self.service_state = CONFIG_OK

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
        if VendorMap[self.device['vendor']] == 'transition':
            template_path = "templates/" + VendorMap[self.device['vendor']].lower(
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
        logging.info(template_path)

        # Generates variables path
        variables_path = "variables/" + self.service.service_type.upper() + ".json"
        variables_path = os.path.join(dir, variables_path)
        logging.info(variables_path)

        try:
            # Set up parameters
            params = {}
            params['mgmt_ip'] = self.device['mgmt_ip'].replace('/32', '')
            params['service_id'] = self.service.service_id
            params['service_type'] = self.service.service_type
            params['client_name'] = self.service.client_name
            params.update(self.service.parameters)
            params['an_port_description'] = "ACTIVO_ID_" + \
                str(self.service.parameters['access_port_services'])
            logging.info(f'params: {params}')

            params = json.loads(render(variables_path, params))
            logging.info(f'parameters to be used: {params}')
        except BaseException as e:
            logging.error(e)
            print(e)
            return

        config_handler = getattr(
            ConfigHandler.ConfigHandler, StrategyMap[VendorMap[self.device['vendor']]])
        logging.info("strategy: " +
                     StrategyMap[VendorMap[self.device['vendor']]])

        try:
            status = config_handler(template_path, params)
            self.task_state = status
        except BaseException as e:
            logging.error(e)
            self.task_state = CONFIG_GENERAL_ERROR
        logging.info(f'Config task state: {self.task_state}')

    def rollback(self):

        dir = os.path.dirname(os.path.abspath(__file__))

        if VendorMap[self.device['vendor']] == 'transition':
            template_path = "templates/" + VendorMap[self.device['vendor']].lower(
            ) + "/" + self.device['model'].lower() + "/" + "DELETE_L2SERVICE.CONF"
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

        logging.info(template_path)
        logging.info(variables_path)

        params = {}
        params['mgmt_ip'] = self.device['mgmt_ip'].replace('/32', '')
        params['service_id'] = self.service.service_id
        params['service_type'] = self.service.service_type
        params['client_name'] = self.service.client_name

        params.update(self.service.parameters)

        params = json.loads(render(variables_path, params))

        config_handler = getattr(
            ConfigHandler.ConfigHandler, StrategyMap[VendorMap[self.device['vendor']]])
        try:
            config_handler(template_path, params)
            self.task_state = CONFIG_ROLLBACK_OK
        except BaseException as e:
            logging.error(e)
            self.task_state = CONFIG_ROLLBACK_ERROR
        logging.debug(f'Rollback state: {self.task_state}')
