from django.db import models

class BaseModel(models.Model):
    class Meta:
        abstract = True

    def fields(self):
        v = vars(self)
        v.pop('_state')
        return v