from django.db import models
from jeangrey.models.base_model import BaseModel
from jeangrey.models.client import Client


class CustomerLocation(BaseModel):
    address = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.address
