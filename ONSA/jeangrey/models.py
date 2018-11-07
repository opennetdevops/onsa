from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Client(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=100, unique=True)
    service_state = models.CharField(max_length=100, null=True)
    service_type = models.CharField(max_length=100, null=True)
    bandwidth = models.CharField(max_length=100, null=True)
   
    location_id = models.CharField(max_length=100, null=True)
    router_node_id = models.CharField(max_length=100, null=True)
    logical_unit_id = models.CharField(max_length=100, null=True)
    access_node_id = models.CharField(max_length=100)
    access_port_id = models.CharField(max_length=100)
    vlan_id = models.CharField(max_length=100) 

    client_node_sn = models.CharField(max_length=100, null=True)
    client_port_id = models.CharField(max_length=100, null=True)        

    class Meta:
        unique_together = (('vlan_id', 'access_node_id', 'access_port_id'),)

    def __str__(self):
        return "SERVICE_ID: " + str(self.id)

class CpelessIrs(Service):
    prefix = models.CharField(max_length=100, null=True)
    public_network = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class CpeIrs(Service):
    prefix = models.CharField(max_length=100, null=True)
    wan_network = models.CharField(max_length=100, null=True)
    public_network = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

class CpelessMpls(Service):
    vrf_id = models.CharField(max_length=100, null=True, blank=True)
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])
    client_network = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.id)

class CpeMpls(Service):
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])
    vrf_id = models.CharField(max_length=100, null=True, blank=True)
    wan_network = models.CharField(max_length=100, null=True)
    client_network = models.CharField(max_length=100, null=True)  

    def __str__(self):
        return str(self.id)

class VcpeIrs(Service):
    prefix = models.CharField(max_length=100, null=True)
    vcpe_logical_unit_id = models.CharField(max_length=100, null=True)
    wan_ip = models.CharField(max_length=100, null=True)
    portgroup_id = models.CharField(max_length=100, null=True)
    public_network = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Vpls(Service):
    vrf_id = models.CharField(max_length=100, null=True, blank=True)
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])

    def __str__(self):
        return str(self.id)

class CustomerLocation(models.Model):
    address = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.address