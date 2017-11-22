from django.db import models

# Create your models here.

class Hub (models.Model):
	name = models.CharField(max_length=50)
	transport_zone_name = models.CharField(max_length=50)
	cluster_name = models.CharField(max_length=50)
	datastore_id = models.CharField(max_length=50)
	resource_pool_id = models.CharField(max_length=50)
	uplink_ip = models.GenericIPAddressField()
	uplink_pg = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Portgroup (models.Model):
	vlan_tag = models.IntegerField()
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)

class Client (models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class PrivateIrsService (models.Model):
	ip_segment = models.GenericIPAddressField()
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	edge_name = models.CharField(max_length=50)

class PublicIrsService (models.Model):
	ip_segment = models.GenericIPAddressField()
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	edge_name = models.CharField(max_length=50)
