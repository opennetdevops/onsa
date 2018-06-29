from django.db import models



# class IpWan(models.Model):
# 	hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
# 	used = models.BooleanField(default=False)
# 	network = models.CharField(max_length=50)
# 	prefix = models.PositiveSmallIntegerField()
# 	ipam_id = models.PositiveSmallIntegerField()
	
# 	def __str__(self):	
# 		return self.network

# 	def get_free_wan_ip_from_hub(hub):
# 		ipWanFree = IpWan.objects.filter(used=False, hub=hub) 
# 		return ipWanFree[0]

# 	def assign_free_wan_ip_from_hub(hub):
# 		ipWanFree = IpWan.objects.filter(used=False, hub=hub) 
# 		ipw = ipWanFree[0]
# 		ipw.used = True
# 		ipw.save()
# 		return ipw

# 	def unassign_ip(network):
# 		ipToRelease = IpWan.objects.get(network=network) 
# 		ipToRelease.used = False
# 		ipToRelease.save()
# 		return

# class IpPublicSegment(models.Model):
# 	used = models.BooleanField(default=False)
# 	ip = models.GenericIPAddressField() 
# 	prefix = models.PositiveSmallIntegerField()
# 	ipam_id = models.PositiveSmallIntegerField()
	
# 	def __str__(self):
# 		return self.ip

# 	def get_free_public_ip():
# 		ipFree = IpPublicSegment.objects.filter(used=False) 
# 		return ipFree[0]

# 	def assign_free_public_ip():
# 		ipFree = IpPublicSegment.objects.filter(used=False) 
# 		ipp = ipFree[0]
# 		ipp.used = True
# 		ipp.save()
# 		return ipp
	
# 	def unassign(self):
# 		self.used = False
# 		self.save()
# 		return



class Client(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Service(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	product_identifier = models.CharField(max_length=50)
	# sco_port = models.OneToOneField(ScoPort, on_delete=models.CASCADE)
	# sco_logical_unit = models.PositiveSmallIntegerField()
	# hub = models.OneToOneField(Hub, on_delete=models.CASCADE)

	class Meta:
		abstract = True

class NsxPublicIrsService (Service):
	# public_network = models.OneToOneField(IpPublicSegment, on_delete=models.CASCADE)
	# public_prefix = models.PositiveSmallIntegerField()
	# vxrail_logical_unit = models.PositiveSmallIntegerField()
	edge_name = models.CharField(max_length=50)
	ip_wan = models.GenericIPAddressField() 
	# portgroup = models.ForeignKey(Portgroup, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.edge_name

class CpeLessIrsService(Service):
	public_network = models.GenericIPAddressField()
	# public_prefix = models.PositiveSmallIntegerField()
		
	def __str__(self):
		pass

class CpeLessMplsService(Service):
	public_network = models.GenericIPAddressField()
	# public_prefix = models.PositiveSmallIntegerField()
	vrf_name = models.CharField(max_length=50)

	def __str__(self):
		pass





