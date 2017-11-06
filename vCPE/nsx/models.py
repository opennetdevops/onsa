from django.db import models

# Create your models here.

class Hub (models.Model):
	name = models.CharField(max_length=50)

class Portgroup (models.Model):
	vlan_tag = models.IntegerField()
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub)

class Client (models.Model)
	name = models.CharField(max_length=50)