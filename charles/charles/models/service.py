from django.db import models
from charles.models.base_model import BaseModel
from charles.exceptions import *

class Service(BaseModel):
    service_id = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50, blank=True, null=True)
    last_state = models.CharField(max_length=50, blank=True, null=True)
    target_state = models.CharField(max_length=50, blank=True, null=True)
    deployment_mode = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.service_id

    def reprocess(self, target_state, deployment_mode):
        self.service_state = self.last_state
        self.target_state = target_state
        self.deployment_mode = deployment_mode
        self.save()




