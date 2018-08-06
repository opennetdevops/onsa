from django.db import models

# Create your models here.
class Service(models.Model):
	service_id = models.CharField(max_length=50)
	service_type = models.CharField(max_length=50)
	service_state = models.CharField(max_length=50) 
	client_id = models.CharField(max_length=50)
	client_name = models.CharField(max_length=50)
	location = models.CharField(max_length=50)

	def __str__(self):
		return self.service_id