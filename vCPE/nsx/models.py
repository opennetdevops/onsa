from django.db import models

# Create your models here.

class Hub (models.Model):
	name = models.CharField(max_length=50)
	transport_zone_name = models.CharField(max_length=50)
	cluster_name = models.CharField(max_length=50)
	datastore_id = models.IntegerField()
	resource_pool_id = models.IntegerField()
	uplink_ip = models.GenericIPAddressField()
	uplink_pg = models.CharField(max_length=50)

class Portgroup (models.Model):
	vlan_tag = models.IntegerField()
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)

class Client (models.Model):
	name = models.CharField(max_length=50)

class PrivateIrsService (models.Model):
	ip_segment = models.GenericIPAddressField()
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)

class PublicIrsService (models.Model):
	ip_segment = models.GenericIPAddressField()
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
