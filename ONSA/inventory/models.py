from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, null=True)  #HUB
    address = models.CharField(max_length=50, blank=True)
    pop_size =  models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=50)
    deviceType = models.CharField(max_length=50, blank=True)
    mgmtIP = models.CharField(max_length=50, blank=True)
    # TODO Change IP to dict() with type key and IP value
    model = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=50, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE) 

    class Meta:
        abstract = True


class AccessNode(Device): #SCO
    uplinkInterface = models.CharField(max_length=50) #AE del lado del MX
    uplink_ports = models.CharField(max_length=50, blank=True)
    accessNodeId = models.CharField(max_length=4) 
    qinqOuterVlan = models.CharField(max_length=50)
    logicalUnitId = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RouterNode(Device): #MX
    privateWanIp = models.GenericIPAddressField(null=True, blank=True) #IP for WAN Virtual CPE
    loopback = models.GenericIPAddressField(null=True, blank=True) 

    def __str__(self):
        return self.name

class ClientNode(Device):
    serial_number = models.CharField(primary_key=True, max_length=50, blank=True, unique=True)
    client = models.CharField(max_length=50, blank=True)
    uplink_port = models.CharField(max_length=50, blank=True)

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
    accessNode = models.ForeignKey(AccessNode, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.accessNode.location) + " - " + self.port



class VlanTag(models.Model):
    vlan_tag = models.CharField(max_length=50,  unique=True)
    vlan_tag.null = True
    access_nodes = models.ManyToManyField(AccessNode, blank=True, through='Products')

    def __str__(self):
        return self.vlan_tag



class VirtualVmwPod(Device):
    uplinkInterface = models.CharField(max_length=50, null=True) #AE del lado del MX
    transportZoneName = models.CharField(max_length=50, blank=True) #TODO NSX Only
    clusterName = models.CharField(max_length=50, blank=True)
    datastoreId = models.CharField(max_length=50, blank=True)
    resourcePoolId = models.CharField(max_length=50, blank=True)
    datacenterId = models.CharField(max_length=50, blank=True)
    uplinkPg = models.CharField(max_length=50, blank=True)
    uplinkPgId = models.CharField(max_length=50, blank=True)
    routerNode = models.OneToOneField(RouterNode, on_delete=models.SET_NULL,null=True) #TODO no me gusta


    def __str__(self):
        return self.clusterName

class Portgroup(models.Model):
    vlan_tag = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    virtualVmwPod = models.ForeignKey(VirtualVmwPod, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    dvportgroup_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class NsxEdge(Device):
    edgeName = models.CharField(max_length=50)
    ipWan = models.CharField(max_length=50)
    portgroup = models.ForeignKey(Portgroup, on_delete=models.CASCADE)

    def delete(self):
        pg = self.portgroup
        pg.used = False
        pg.save()
        super(NsxEdge, self).delete()

    def __str__(self):
        return self.edgeName


class LogicalUnit(models.Model):
    logical_unit_id = models.PositiveSmallIntegerField(unique=True)
    routerNodes = models.ManyToManyField(RouterNode, blank=True) 
    product_id = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return str(self.logical_unit_id)



class Vrf(models.Model):
    locations = models.ManyToManyField(Location, blank=True) 
    rt = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    used = models.BooleanField(default=False)
    description = models.CharField(max_length=50, null=True)
    client = models.CharField(max_length=50, null=True, blank=True)


class Products(models.Model):
    vlantag = models.ForeignKey(VlanTag, models.DO_NOTHING)
    access_node = models.ForeignKey(AccessNode, models.DO_NOTHING)
    product_id = models.CharField(max_length=50, blank=True, unique=True, null=True)
    client_node_sn = models.CharField(max_length=50, null=True)
    client_node_port = models.CharField(max_length=50, null=True)
    bandwidth = models.CharField(max_length=50, null=True)
    access_port_id = models.CharField(max_length=50)
    vrf_id = models.CharField(max_length=50, null=True, blank=True)
    # site_id = models.CharField(max_length=50)

    class Meta:
        unique_together = (('vlantag', 'access_node', 'access_port_id'),)

    def __str__(self):
        return self.access_node.name + \
        " - Vlan: " + self.vlantag.vlan_tag + " - Product Id: " + self.service_id

