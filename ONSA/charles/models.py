from django.db import models
from charles.utils.fsm import Fsm
from charles.utils.utils import *


# Create your models here.
class Service(models.Model):
    service_id = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50, blank=True, null=True)
    target_state = models.CharField(max_length=50, blank=True, null=True)
    deployment_mode = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.service_id

    def process_worker_response(self, state):
        if state != "ERROR":
            #move to the next state
            self.service_state = Fsm.to_next_state(my_service)
            self.save()
            if self.service_state != self.target_state:
                self.service_state = FSM.run(my_service)
        else:
            self.service_state = "error"
            self.save()
        
        return self.service_state



