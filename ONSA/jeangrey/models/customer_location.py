from django.db import models
from jeangrey.models.client import Client

class CustomerLocation(models.Model):
    address = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.address