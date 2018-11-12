from django.db import models



# Create your models here.
class Service(models.Model):
    service_id = models.CharField(max_length=50)
    service_state = models.CharField(max_length=50, blank=True, null=True)
    target_state = models.CharField(max_length=50, blank=True, null=True)
    deployment_mode = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.service_id



