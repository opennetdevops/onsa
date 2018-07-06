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

    """
    REMOVE
    Will be handled in views/access_nodes.py
    """    
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

    def get_free_logical_units(self):
        lus_free = LogicalUnit.objects.exclude(locations=self)
        return lus_free

    def get_used_logical_units(self):
        lus_Used = Location.objects.filter(locations=self)
        return lus_Used

    def assign_free_logical_unit(self):
        lus_free = Location.objects.exclude(locations=self) 
        lu = lus_free[0]
        lu.locations.add(self)       
        lu.save()
        return lu

    def assign_free_logical_unit(self):
        lus_free = Location.objects.exclude(locations=self) 
        lu = lus_free[0]
        lu.locations.add(self)       
        lu.save()
        return lu

    def remove_logical_unit(self, logical_unit_id):
        lu = LogicalUnit.objects.get(logical_unit_id=logical_unit_id)
        lu.locations.remove(self)
        lu.save()
        return lu

    def assign_logical_unit(self, logical_unit_id):
        lu = LogicalUnit.objects.get(logical_unit_id=logical_unit_id)
        lu.locations.add(self)
        lu.save()
        return lu

    """
    REMOVE
    Will be handled in views/access_nodes.py
    """
    def delete_access_node(self, accessNodeId):
        an = AccessNode.objects.get(location=self,accessNodeId=accessNodeId)
        an.delete()
        return 

    """
    REMOVE
    Will be handled in views/router_nodes.py
    """  
    def add_router_node(self, name, mgmtIP, model, accessNodeId, privateWanIp):
        router_node = RouterNode(name=name, deviceType="RouterNode", mgmtIP=mgmtIP, location=self,
            model=model, privateWanIp=privateWanIp)
        router_node.save()
        return

    """
    REMOVE
    Will be handled in views/router_nodes.py
    """ 
    def delete_router_node(self):
        rn = self.get_router_node()
        rn.delete()
        return

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

    def add_virtual_vmw_pod(self):
        pass


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
    vlan_tag = models.CharField(max_length=50,  unique=True)
    vlan_tag.null = True
    accessPorts = models.ManyToManyField(AccessPort)

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
    logical_unit_id = models.PositiveSmallIntegerField(unique=True)
    locations = models.ManyToManyField(Location)

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

