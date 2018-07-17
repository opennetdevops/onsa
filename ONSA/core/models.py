from django.db import models




class Client(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cpe(models.Model):
    serial_number = models.CharField(max_length=50)
    ip_management = models.GenericIPAddressField()

    def __str__():
        return self.serial_number

class CpePort(models.Model):
    name = models.CharField(max_length=50)
    cpe = models.ForeignKey(Cpe, on_delete=models.CASCADE, null=True)

class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    service_id = models.CharField(max_length=50, unique=True)
    product_identifier = models.CharField(max_length=50)
    bandwidth = models.PositiveSmallIntegerField()
    
    
    STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("REQUESTED", "REQUESTED"),
    ("COMPLETED", "COMPLETED"),
    ("ERROR", "ERROR")
    )
    
    SERVICE_TYPES = (
    ("PUBLIC_IRS_VCPE", "PUBLIC_IRS_VCPE"),
    ("MPLS", "MPLS"),
    ("VPLS", "VPLS"),
    ("PUBLIC_IRS_CPELESS", "PUBLIC_IRS_CPELESS"),
    )

    service_type = models.CharField(max_length=30,
                  choices=SERVICE_TYPES,
                  default="PUBLIC_IRS_CPELESS")

    status = models.CharField(max_length=15,
                  choices=STATUS_CHOICES,
                  default="PENDING")

    class Meta:
        abstract = True




class PublicIrsService (Service):
    
    edge_name = models.CharField(max_length=50,blank=True)
    ip_wan = models.GenericIPAddressField() 
    cpe_port = models.OneToOneField(CpePort, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return "Public IRS Service" + self.edge_name



class CpeLessIrsService(Service):

    public_network = models.GenericIPAddressField()
        
    def __str__(self):
        return "CPE Less IRS Service" + self.public_network



class MplsService(Service):

    public_network = models.GenericIPAddressField()
    vrf_name = models.CharField(max_length=50)
    cpe_port = models.ForeignKey(CpePort, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return "MPLS Service" + self.vrf_name





