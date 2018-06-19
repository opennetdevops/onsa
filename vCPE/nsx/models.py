from django.db import models

class Hub (models.Model):
	name = models.CharField(max_length=50)
	transport_zone_name = models.CharField(max_length=50)
	cluster_name = models.CharField(max_length=50)
	datastore_id = models.CharField(max_length=50)
	resource_pool_id = models.CharField(max_length=50)
	datacenter_id = models.CharField(max_length=50)
	uplink_ip = models.GenericIPAddressField()
	uplink_pg = models.CharField(max_length=50)
	uplink_pg_id = models.CharField(max_length=50)
	mx_ip = models.GenericIPAddressField()
	vxrail_ae_interface = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class LogicalUnit (models.Model):
	logical_unit_id = models.PositiveSmallIntegerField()
	hubs = models.ManyToManyField(Hub)
	used = models.BooleanField(default=False)

	def __str__(self):
		return str(self.logical_unit_id)

	def assign_free_logical_unit_at_hub(hub):
		free_logical_unit = LogicalUnit.objects.filter(used=False,hubs=hub)
		logical_unit = free_logical_unit[0] 
		logical_unit.used = True
		logical_unit.save()
		logical_unit.hubs.add(hub)
		return logical_unit

	def get_free_logical_unit_from_hub(hub):
		free_logical_unit = LogicalUnit.objects.filter(used=False,hubs=hub)
		return free_logical_unit

	def unassign(logical_unit, hub):
		logical_unit = LogicalUnit.objects.filter(used=True,hubs=hub,logical_unit_id=logical_unit)
		logical_unit_to_release = logical_unit[0]
		logical_unit_to_release.used = False
		logical_unit_to_release.save()
		return

class Sco(models.Model):
	name = models.CharField(max_length=50)
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
	sco_id = models.CharField(max_length=4)
	sco_ae_interface = models.CharField(max_length=50)
	sco_outer_vlan = models.CharField(max_length=50)


	def __str__(self):
		return self.name

class ScoPort(models.Model):
	description = models.CharField(max_length=50)
	
	port = models.CharField(max_length=50)
	port.null = True

	used = models.BooleanField(default=False)
	sco = models.ForeignKey(Sco, on_delete=models.CASCADE)
	vlan_tag = models.CharField(max_length=50)
	vlan_tag.null = True
	

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
	dvportgroup_id = models.CharField(max_length=50)

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
	product_identifier = models.CharField(max_length=50)
	sco_port = models.OneToOneField(ScoPort, on_delete=models.CASCADE)
	sco_logical_unit = models.PositiveSmallIntegerField()

	class Meta:
		abstract = True


#
# @ip_segment: Private IP Addressing used at customer location
#
# class PrivateIrsService (Service):
# 	ip_segment = models.GenericIPAddressField()

# 	def __str__(self):
# 		return self.client.name

class NsxPublicIrsService (Service):
	public_network = models.OneToOneField(IpPublicSegment, on_delete=models.CASCADE)
	vxrail_logical_unit = models.PositiveSmallIntegerField()
	edge_name = models.CharField(max_length=50)
	ip_wan = models.CharField(max_length=50)
	portgroup = models.OneToOneField(Portgroup, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.client.name

class CpeLessIrsService(Service):
	public_network = models.OneToOneField(IpPublicSegment, on_delete=models.CASCADE)
	ip_wan = models.CharField(max_length=50)
	client_unit = models.PositiveSmallIntegerField()

	def __str__(self):
		return self.client_name





