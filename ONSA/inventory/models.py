from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=50, blank=True)  #HUB
    address = models.CharField(max_length=50, blank=True) 

    def __str__(self):
        return self.name

    def get_router_nodes(self):
        router_nodes = RouterNode.objects.filter(deviceType="RouterNode",location=self)
        return router_nodes

    def get_access_nodes(self):
        access_nodes = AccessNode.objects.filter(deviceType="AccessNode",location=self)
        return access_nodes


class Device(models.Model):
    name = models.CharField(max_length=50)
    deviceType = models.CharField(max_length=50, blank=True)
    mgmtIP = models.CharField(max_length=50, blank=True)
    # TODO Change IP to dict() with type key and IP value
    model = models.CharField(max_length=50, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE) 

    class Meta:
        abstract = True


class AccessNode(Device): #SCO
    uplinkInterface = models.CharField(max_length=50) #AE del lado del MX
    accessNodeId = models.CharField(max_length=4) 
    qinqOuterVlan = models.CharField(max_length=50)
    logicalUnitId = models.CharField(max_length=50)

    def get_access_ports(self):
        access_ports = AccessPort.objects.filter(accessNode=self)
        return access_ports

    def get_free_access_ports(self):
        access_ports = AccessPort.objects.filter(accessNode=self, used=False)
        access_port = access_ports[0]
        return access_port

    def __str__(self):
        return self.name


class RouterNode(Device): #MX
    privateWanIp = models.GenericIPAddressField(null=True, blank=True) #IP for WAN Virtual CPE


    def get_free_logical_units(self):
        lus_free = LogicalUnit.objects.exclude(routerNodes=self)
        return lus_free

    def get_used_logical_units(self):
        lus_Used = Location.objects.filter(routerNodes=self)
        return lus_Used

    def __str__(self):
        return self.name

class ClientNode(Device):
    serialNumber = models.CharField(max_length=50, blank=True)
    client = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.serialNumber

class OpticalNode(Device):
    serialNumber = models.CharField(max_length=50, blank=True)
    client = models.CharField(max_length=50, blank=True)
    hwId = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.serialNumber

class AccessPort(models.Model):
    description = models.CharField(max_length=50)
    port = models.CharField(max_length=50)
    port.null = True
    used = models.BooleanField(default=False)
    accessNode = models.ForeignKey(AccessNode, on_delete=models.CASCADE)
    client = models.CharField(max_length=50, blank=True)
    client.null = True


    def __str__(self):
        return str(self.accessNode.location) + " - " + self.port

    def get_vlan_tags(self):
        vlan_tags = VlanTag.objects.filter(accessPorts=self)
        return vlan_tags


    def unassign(self):
        self.used = False
        #todo remove all vlan assoc
        vlans = self.get_used_vlans()
        for i in vlans:
            i.access_ports.remove(self)
        self.save()
        return

    def get_free_vlans(self):
        vlansFree = VlanTag.objects.exclude(accessPorts=self)
        return vlansFree

    def get_used_vlans(self):
        vlansUsed = VlanTag.objects.filter(accessPorts=self)
        return vlansUsed


    def assign_free_vlan(self):
        vlansFree = VlanTag.objects.exclude(accessPorts=self) 
        vlan = vlansFree[0]
        vlan.accessPorts.add(self)       
        vlan.save()
        return vlan

    def assign_vlan(self, vlanId):
        vlan = VlanTag.objects.filter(vlan_tag=vlanId)
        #todo error already assigned
        vlan.accessPorts.add(self)
        vlan.save()
        return True


class VlanTag(models.Model):
    vlan_tag = models.CharField(max_length=50,  unique=True)
    vlan_tag.null = True
    accessPorts = models.ManyToManyField(AccessPort, blank=True, through='VlantagAccessports')

    def __str__(self):
        return self.vlan_tag


    def initialize():
        #TODO GLOBAL VARIABLE
        vlans_per_port = 10
        initial_vlan_tag_id = 1800

        for i in range(vlans_per_port):
            VlanTag.add(initial_vlan_tag_id+i)
        return

    def add(vlanId):
        vlan = VlanTag(vlan_tag=vlanId)
        vlan.save()
        return


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


    def get_free_pg_from_virtualVmwPod(virtualVmwPod):
        portgroupsFree = Portgroup.objects.filter(used=False, virtualVmwPod=virtualVmwPod) 
        return portgroupsFree[0]

    def unassign(self):
        self.used = False
        self.save()
        return


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

    def __str__(self):
        return str(self.logical_unit_id)

    def initialize():
        #TODO GLOBAL VARIABLE
        logical_units_per_location = 100
        initial_logical_unit_id = 10000

        for i in range(logical_units_per_location):
            LogicalUnit.add(initial_logical_unit_id+i)
        return

    def add(logical_unit_id):
        logical_unit = LogicalUnit(logical_unit_id=logical_unit_id)
        logical_unit.save()
        return

class VlantagAccessports(models.Model):
    vlantag = models.ForeignKey(VlanTag, models.DO_NOTHING)
    accessport = models.ForeignKey(AccessPort, models.DO_NOTHING)
    serviceid = models.CharField(max_length=50, unique=True, blank=True)
    sn_client_node = models.CharField(max_length=50)
    client_node_port = models.CharField(max_length=50)
    bandwidth = models.CharField(max_length=50)

    class Meta:
        db_table = 'inventory_vlantag_accessPorts'
        unique_together = (('vlantag', 'accessport'),)

    def __str__(self):
        return self.accessport.accessNode.name + " - Port: " +self.accessport.port + \
        " - Vlan: " + self.vlantag.vlan_tag + " - Service Id: " + self.serviceid

