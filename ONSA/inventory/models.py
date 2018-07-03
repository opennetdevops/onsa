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

    def get_access_nodes(self):
        access_nodes = AccessNode.objects.filter(deviceType="AccessNode",location=self)
        return access_nodes

    def add_access_node(self, name, mgmtIP, model, accessNodeId, uplinkInterface="ae1",
        qinqOuterVlan="1", ports=24, ifPattern="eth1/"):

        #By default QinQ-Outer-VLAN is equal to the access Node (even if they say the opposite)
        access_node = AccessNode(name=name, deviceType="AccessNode", mgmtIP=mgmtIP, model=model,
            location=self, uplinkInterface=uplinkInterface, accessNodeId=accessNodeId,
            qinqOuterVlan=accessNodeId)
        access_node.save()

        for i in ports:
            port_name = ifPattern + "i"
            access_port = AccessPort(port=port_name, used=False, accessNode=access_node)
            access_port.save()
        return

    def delete_access_node():
        pass

    def get_free_logical_unit(self):
        return LogicalUnit.get_free_logical_unit_from_location(self)
    
    def get_free_logical_units(self):     
        return LogicalUnit.get_free_logical_units_from_location(self)    



    def add_router_node(self):
        pass








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

    def add(name, mgmtIP, model, accessNodeId, location, uplinkInterface="ae1",
        qinqOuterVlan="1", ports=24, ifPattern="eth0/"):

        #By default QinQ-Outer-VLAN is equal to the access Node (even if they say the opposite)
        access_node = AccessNode(name=name, deviceType="AccessNode", mgmtIP=mgmtIP, model=model,
            location=location, uplinkInterface=uplinkInterface, accessNodeId=accessNodeId,
            qinqOuterVlan=accessNodeId)
        access_node.save()

        for i in range(ports):
            port_name = ifPattern + str(i)
            print(port_name)
            access_port = AccessPort.add(port_name,access_node)
        return access_node


    def get_access_ports_from_node(self):
        access_ports = AccessPort.objects.filter(accessNode=self)
        return access_ports

    def get_free_access_port_from_node(self):
        access_ports = AccessPort.objects.filter(accessNode=self, used=False)
        access_port = access_ports[0]
        return access_port

    def assign_free_access_port_from_node(self):
        access_ports = AccessPort.objects.filter(accessNode=self, used=False)
        access_port = access_ports[0]
        access_port.used = True
        access_port.save()
        return access_port


    def __str__(self):
        return self.name

class RouterNode(Device): #MX
    privateWanIp = models.GenericIPAddressField(null=True, blank=True)

    # def add_router_node(name)
    
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
        return str(self.accessNode.location) + " - " + self.port

    # def delete(self):
    #     self.unassign()
    #     super(AccessPort, self).delete()


    def add(port_name, access_node):
        access_port = AccessPort(port=port_name, used=False, accessNode=access_node)
        access_port.save()
        return access_port


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
    vlan_tag = models.CharField(max_length=50)
    vlan_tag.null = True
    accessPorts = models.ManyToManyField(AccessPort)
    # used = models.BooleanField(default=False)


    def __str__(self):
        return self.vlan_tag

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
    def initialize():
        #TODO GLOBAL VARIABLE
        vlans_per_port = 10
        initial_vlan_tag_id = 1800

        for i in range(vlans_per_port):
            VlanTag.add(initial_vlan_tag_id+i)
        return

    def add(vlanId):
        if VlanTag.objects.filter(vlan_tag=vlanId).count() > 0: return
        vlan = VlanTag(vlan_tag=vlanId)
        vlan.save()
        return



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
        logical_unit = free_logical_unit[0] 
        return logical_unit

    def get_free_logical_units_from_location(location):
        free_logical_unit = LogicalUnit.objects.filter(used=False,locations=location)
        return free_logical_unit

    def unassign(logical_unit, location):
        logical_unit = LogicalUnit.objects.filter(used=True,locations=location,logical_unit_id=logical_unit)
        logical_unit_to_release = logical_unit[0]
        logical_unit_to_release.used = False
        logical_unit_to_release.save()
        return
