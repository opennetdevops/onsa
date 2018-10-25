from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Client(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    service_state = models.CharField(max_length=15, null=True)
    service_type = models.CharField(max_length=30, null=True)
    bandwidth = models.CharField(max_length=50, null=True)
    prefix = models.CharField(max_length=50, null=True)

    location_id = models.CharField(max_length=10, null=True)
    router_node_id = models.CharField(max_length=10, null=True)
    logical_unit_id = models.CharField(max_length=10, null=True)
    access_node_id = models.CharField(max_length=10)
    access_port_id = models.CharField(max_length=50)
    vlan_id = models.CharField(max_length=10) 

    client_node_sn = models.CharField(max_length=50, null=True)
    client_port_id = models.CharField(max_length=50, null=True)        

    class Meta:
        unique_together = (('vlan_id', 'access_node_id', 'access_port_id'),)

    def __str__(self):
        return "SERVICE_ID: " + str(self.id)

class CpelessIrs(Service):
    public_network = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class CpeIrs(Service):
    wan_network = models.CharField(max_length=50)
    public_network = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

class CpelessMpls(Service):
    vrf_id = models.CharField(max_length=50, null=True, blank=True)
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])
    client_network = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.id)

class CpeMpls(Service):
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])
    vrf_id = models.CharField(max_length=50, null=True, blank=True)
    wan_network = models.CharField(max_length=50)
    client_network = models.CharField(max_length=50, blank=True)  

    def __str__(self):
        return str(self.id)

class VcpeIrs(Service):
    vcpe_logical_unit_id = models.CharField(max_length=10, null=True)
    wan_ip = models.CharField(max_length=50, null=True)
    portgroup_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.id)

class Vpls(Service):
    vrf_id = models.CharField(max_length=50, null=True, blank=True)
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])

    def __str__(self):
        return str(self.id)