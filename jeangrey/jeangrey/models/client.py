from django.db import models
from jeangrey.models.base_model import BaseModel

class Client(BaseModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name