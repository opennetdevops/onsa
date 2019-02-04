from django.db import models
from charles.utils.fsm import Fsm
from charles.utils.utils import *

class Service(models.Model):
    service_id = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50, blank=True, null=True)
    last_state = models.CharField(max_length=50, blank=True, null=True)
    target_state = models.CharField(max_length=50, blank=True, null=True)
    deployment_mode = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.service_id

    def reprocess(self):
        #If service already exists (in error state), just modify his initial state
        if self.service_state == "error":
            self.service_state = self.last_state
            self.save()
        else:
            raise ServiceException("Unable to reprocess requested service id")



