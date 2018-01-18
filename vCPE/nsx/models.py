from django.db import models

# Create your models here.

class Hub (models.Model):
	name = models.CharField(max_length=50)
	transport_zone_name = models.CharField(max_length=50)
	cluster_name = models.CharField(max_length=50)
	datastore_id = models.CharField(max_length=50)
	resource_pool_id = models.CharField(max_length=50)
	datacenter_id = models.CharField(max_length=50)
	#gateway ip
	uplink_ip = models.GenericIPAddressField()
	uplink_pg = models.CharField(max_length=50)
	mx_ip = models.GenericIPAddressField()

	def __str__(self):
		return self.name



class Sco(models.Model):
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	# sco_id = models.CharField(max_length=4)

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

	def get_free_port_from_sco(sco):
		portsFree = ScoPort.objects.filter(used=False, sco=sco) 
		return portsFree[0]

	def assign_free_port_from_sco(sco):
		portsFree = ScoPort.objects.filter(used=False, sco=sco) 
		scoport = portsFree[0]
		scoport.used = True
		scoport.save()
		return scoport

	def unassign(self):
		self.used = False
		self.save()
		return





class IpWan (models.Model):
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)
	network = models.CharField(max_length=50)
	prefix = models.PositiveSmallIntegerField()
	
	def __str__(self):
		return self.network

	def get_free_wan_ip_from_hub(hub):
		ipWanFree = IpWan.objects.filter(used=False, hub=hub) 
		return ipWanFree[0]

	def assign_free_wan_ip_from_hub(hub):
		ipWanFree = IpWan.objects.filter(used=False, hub=hub) 
		ipw = ipWanFree[0]
		ipw.used = True
		ipw.save()
		return ipw

	def unassign_ip(network):
		ipToRelease = IpWan.objects.get(network=network) 
		ipToRelease.used = False
		ipToRelease.save()
		return




class IpPublicSegment (models.Model):
	used = models.BooleanField(default=False)
	ip = models.GenericIPAddressField() 
	prefix = models.PositiveSmallIntegerField()
	
	def __str__(self):
		return self.ip

	def get_free_public_ip():
		ipFree = IpPublicSegment.objects.filter(used=False) 
		return ipFree[0]

	def assign_free_public_ip():
		ipFree = IpPublicSegment.objects.filter(used=False) 
		ipp = ipFree[0]
		ipp.used = True
		ipp.save()
		return ipp
	
	def unassign(self):
		self.used = False
		self.save()
		return



class Portgroup (models.Model):
	vlan_tag = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def get_free_pg_from_hub(hub):
		portgroupsFree = Portgroup.objects.filter(used=False, hub=hub) 
		return portgroupsFree[0]

	def assign_free_pg_from_hub(hub):
		portgroupsFree = Portgroup.objects.filter(used=False, hub=hub)
		port_free = portgroupsFree[0] 
		port_free.used = True
		port_free.save()
		return port_free

	def unassign(self):
		self.used = False
		self.save()
		return


class Client (models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name



class Service(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	edge_name = models.CharField(max_length=50)
	ip_wan = models.CharField(max_length=50)
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

	public_network = models.OneToOneField(IpPublicSegment)

	def __str__(self):
		return self.client.name





