from django.db import models

# Create your models here.

class Hub (models.Model):
	name = models.CharField(max_length=50)
	transport_zone_name = models.CharField(max_length=50)
	cluster_name = models.CharField(max_length=50)
	datastore_id = models.CharField(max_length=50)
	resource_pool_id = models.CharField(max_length=50)
	#gateway ip
	uplink_ip = models.GenericIPAddressField()
	uplink_pg = models.CharField(max_length=50)
	mx_ip = models.GenericIPAddressField()

	def __str__(self):
		return self.name



class Sco(models.Model):
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)

	def __str__(self):
		return self.name



class ScoPort(models.Model):
	description = models.CharField(max_length=50)
	port = models.CharField(max_length=50)
	used = models.BooleanField(default=False)
	sco = models.ForeignKey(Sco, on_delete=models.CASCADE)
	vlan_tag = models.CharField(max_length=50)
	vlan_tag.null = True
	port.null = True

	def __str__(self):
		return self.description





class IpWan (models.Model):
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)
	network = models.GenericIPAddressField()
	
	def __str__(self):
		return "network"



class IpPublicSegment (models.Model):
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)
	ip = models.GenericIPAddressField()
	mask = models.PositiveSmallIntegerField()
	
	def __str__(self):
		return self.ip



class Portgroup (models.Model):
	vlan_tag = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)

	def __str__(self):
		return self.name



class Client (models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name



class Service(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	edge_name = models.CharField(max_length=50)
	ip_wan = models.GenericIPAddressField()
	ip_wan.default = "0.0.0.0"
	portgroup = models.OneToOneField(Portgroup)
	sco_port = models.OneToOneField(ScoPort)

	class Meta:
		abstract = True


#
# @ip_segment: Private IP Addressing used at customer location
#
class PrivateIrsService (Service):
	ip_segment = models.GenericIPAddressField()

	def __str__(self):
		return self.client.name


class PublicIrsService (Service):
	ip_segment = models.GenericIPAddressField()
	def __str__(self):
		return self.client.name





