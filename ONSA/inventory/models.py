from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=True)  #HUB
    address = models.CharField(max_length=50, blank=True)
    pop_size =  models.CharField(max_length=50, blank=True)

    def get_router_nodes(self):
        router_nodes = RouterNode.objects.filter(device_type="RouterNode",location=self)
        return router_nodes
    
    def get_access_nodes(self):
        access_nodes = AccessNode.objects.filter(device_type="AccessNode",location=self)
        return access_nodes

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=50)
    device_type = models.CharField(max_length=50, blank=True)
    mgmt_ip = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=50, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE) 

    class Meta:
        abstract = True


class AccessNode(Device): #SCO
    uplink_interface = models.CharField(max_length=50) #AE del lado del MX
    uplink_ports = models.CharField(max_length=50, blank=True)
    access_node_id = models.CharField(max_length=4) 
    provider_vlan = models.CharField(max_length=50)
    logical_unit_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RouterNode(Device): #MX
    private_wan_ip = models.GenericIPAddressField(null=True, blank=True) #IP for WAN Virtual CPE
    loopback = models.GenericIPAddressField(null=True, blank=True) 

    def __str__(self):
        return self.name

class ClientNode(Device):
    serial_number = models.CharField(primary_key=True, max_length=50, blank=True, unique=True)
    client = models.CharField(max_length=50, blank=True, null=True)
    uplink_port = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.serial_number


class ClientNodePort(models.Model):
    interface_name = models.CharField(max_length=50, blank=True)
    client_node = models.ForeignKey(ClientNode, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    service_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.interface_name

class AccessPort(models.Model):
    port = models.CharField(max_length=50)
    port.null = True
    used = models.BooleanField(default=False)
    access_node = models.ForeignKey(AccessNode, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.access_node.location) + " - " + self.port

class VlanTag(models.Model):
    vlan_tag = models.CharField(max_length=50, unique=True)
    vlan_tag.null = True
    access_nodes = models.ManyToManyField(AccessNode, blank=True)

    def __str__(self):
        return self.vlan_tag

class VirtualVmwPod(Device):
    uplink_interface = models.CharField(max_length=50, null=True) #AE del lado del MX
    transport_zone_name = models.CharField(max_length=50, blank=True) #TODO NSX Only
    cluster_name = models.CharField(max_length=50, blank=True)
    datastore_id = models.CharField(max_length=50, blank=True)
    respool_id = models.CharField(max_length=50, blank=True)
    datacenter_id = models.CharField(max_length=50, blank=True)
    uplink_pg = models.CharField(max_length=50, blank=True)
    uplink_pg_id = models.CharField(max_length=50, blank=True)
    router_node = models.OneToOneField(RouterNode, on_delete=models.SET_NULL,null=True) #TODO no me gusta


    def __str__(self):
        return self.cluster_name

class Portgroup(models.Model):
    vlan_tag = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    vmw_pod = models.ForeignKey(VirtualVmwPod, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    dvportgroup_id = models.CharField(max_length=50)
    product_id = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.name


class NsxEdge(Device):
    edge_name = models.CharField(max_length=50)
    ip_wan = models.CharField(max_length=50)
    portgroup = models.ForeignKey(Portgroup, on_delete=models.CASCADE)

    def delete(self):
        pg = self.portgroup
        pg.used = False
        pg.save()
        super(NsxEdge, self).delete()

    def __str__(self):
        return self.edge_name


class LogicalUnit(models.Model):
    logical_unit_id = models.PositiveSmallIntegerField(unique=True)
    router_nodes = models.ManyToManyField(RouterNode, blank=True) 

    def __str__(self):
        return str(self.logical_unit_id)



class Vrf(models.Model):
    locations = models.ManyToManyField(Location, blank=True) 
    rt = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    used = models.BooleanField(default=False)
    description = models.CharField(max_length=50, null=True)
    client = models.CharField(max_length=50, null=True, blank=True)
