from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50, blank=True)  #HUB
    address = models.CharField(max_length=50, blank=True) 

    def __str__(self):
        return self.name

    def get_router_node(self):
        router_node = RouterNode.objects.filter(deviceType="RouterNode",location=self)
        node = router_node[0]
        return node




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
    uplinkInterface = models.CharField(max_length=50)
    accessNodeId = models.CharField(max_length=4)
    qinqOuterVlan = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class RouterNode(Device): #MX
    privateWanIp = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class ClientNode(Device):
    serialNumber = models.CharField(max_length=50, blank=True)
    client = models.CharField(max_length=50, blank=True)
    service = models.CharField(max_length=50, blank=True) #TODO Services (plural, multiple)



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
        return self.description

    def get_free_port_from_accessNode(accessNode):
        portsFree = accessPort.objects.filter(used=False, accessNode=accessNode) 
        return portsFree[0]

    def assign_free_port_from_accessNode(accessNode):
        portsFree = accessPort.objects.filter(used=False, accessNode=accessNode) 
        accport = portsFree[0]
        accport.used = True
        accport.save()
        return accport

    def unassign(self):
        self.used = False
        self.save()
        return

    def assign_free_vlan(self):
        vlansFree = vlanTag.objects.filter(used=False, accessPorts=self) 
        accport = vlansFree[0]
        accport.used = True
        accport.save()
        return accport

    def assign_vlan(self, vlanId):
        vlan = vlanTag(used=True, vlan_tag=vlanId, accessNode=self)
        vlan.save()
        return vlan


class VlanTag(models.Model):
    vlan_tag = models.CharField(max_length=50)
    vlan_tag.null = True
    accessPorts = models.ManyToManyField(AccessPort)
    used = models.BooleanField(default=False)

    # def assign_free_vlan_at_location(location):
    #     free_logical_unit = LogicalUnit.objects.filter(used=False,locations=location)
    #     logical_unit = free_logical_unit[0] 
    #     logical_unit.used = True
    #     logical_unit.save()
    #     logical_unit.locations.add(location)
    #     return logical_unit

    # def get_free_logical_unit_from_location(location):
    #     free_logical_unit = LogicalUnit.objects.filter(used=False,locations=location)
    #     return free_logical_unit

    # def unassign(logical_unit, location):
    #     logical_unit = LogicalUnit.objects.filter(used=True,locations=location,logical_unit_id=logical_unit)
    #     logical_unit_to_release = logical_unit[0]
    #     logical_unit_to_release.used = False
    #     logical_unit_to_release.save()
    #     return



class VirtualVmwPod(Device):
    location = models.CharField(max_length=50, blank=True)  #HUB
    transportZoneName = models.CharField(max_length=50, blank=True) #TODO NSX Only
    clusterName = models.CharField(max_length=50, blank=True)
    datastoreId = models.CharField(max_length=50, blank=True)
    resourcePoolId = models.CharField(max_length=50, blank=True)
    datacenterId = models.CharField(max_length=50, blank=True)

    uplinkPg = models.CharField(max_length=50, blank=True)
    uplinkPgId = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.client.name


class NsxEdge(Device):
    edgeName = models.CharField(max_length=50)
    ipWan = models.CharField(max_length=50)


    def __str__(self):
        return self.client.name

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

    def assign_free_pg_from_virtualVmwPod(virtualVmwPod):
        portgroupsFree = Portgroup.objects.filter(used=False, virtualVmwPod=virtualVmwPod)
        port_free = portgroupsFree[0] 
        port_free.used = True
        port_free.save()
        return port_free

    def unassign(self):
        self.used = False
        self.save()
        return


class LogicalUnit(models.Model):
    logical_unit_id = models.PositiveSmallIntegerField()
    locations = models.ManyToManyField(Location)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.logical_unit_id)

    def assign_free_logical_unit_at_location(location):
        free_logical_unit = LogicalUnit.objects.filter(used=False,locations=location)
        logical_unit = free_logical_unit[0] 
        logical_unit.used = True
        logical_unit.save()
        logical_unit.locations.add(location)
        return logical_unit

    def get_free_logical_unit_from_location(location):
        free_logical_unit = LogicalUnit.objects.filter(used=False,locations=location)
        return free_logical_unit

    def unassign(logical_unit, location):
        logical_unit = LogicalUnit.objects.filter(used=True,locations=location,logical_unit_id=logical_unit)
        logical_unit_to_release = logical_unit[0]
        logical_unit_to_release.used = False
        logical_unit_to_release.save()
        return
