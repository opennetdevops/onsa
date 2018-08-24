from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cpe(models.Model):
    serial_number = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    ip_management = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True) 

    def __str__(self):
        return self.serial_number


class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    product_identifier = models.CharField(max_length=50)
    bandwidth = models.PositiveSmallIntegerField()
    vrf = models.CharField(max_length=50, blank=True)
    prefix = models.CharField(max_length=50, blank=True)
    public_network = models.CharField(max_length=50, blank=True)
    
    SERVICE_STATE_CHOICES = (
    ("PENDING", "PENDING"),
    ("REQUESTED", "REQUESTED"),
    ("COMPLETED", "COMPLETED"),
    ("ERROR", "ERROR")
    )
    
    SERVICE_TYPES = (
    ("vcpe_irs", "vcpe_irs"),
    ("mpls", "mpls"),
    ("vpls", "vpls"),
    ("cpeless_irs", "cpeless_irs"),
    )

    service_type = models.CharField(max_length=30,
                  choices=SERVICE_TYPES,
                  default="cpeless_irs")

    service_state = models.CharField(max_length=15,
                  choices=SERVICE_STATE_CHOICES,
                  default="PENDING")

    def __str__(self):
        return "SERVICE_ID: " + str(self.pk)

class CpePort(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    cpe = models.ForeignKey(Cpe, on_delete=models.CASCADE, null=True)
    services = models.ManyToManyField(Service, blank=True, through='ServiceCpeRelations')

    def __str__(self):
        return "CPE: " + self.cpe.name + " - CPE Port: " + self.name

class VcpeManager(models.Manager):
    def get_queryset(self):
        return super(FeatureManager, self).get_queryset().filter(service_type='vcpe_irs')

class CpeLessIrsManager(models.Manager):
    def get_queryset(self):
        return super(FeatureManager, self).get_queryset().filter(service_type='cpeless_irs')

class MplsManager(models.Manager):
    def get_queryset(self):
        return super(FeatureManager, self).get_queryset().filter(service_type='MPLS')



class VcpePublicIrsService (Service):
    objects = VcpeManager()    

    class Meta:
        proxy = True


class CpeLessIrsService(Service):
    objects = CpeLessIrsManager()    

    class Meta:
        proxy = True



class MplsService(Service):
    objects = MplsManager()    

    class Meta:
        proxy = True


class ServiceCpeRelations(models.Model):
    cpe_port = models.ForeignKey(CpePort, models.DO_NOTHING)
    service = models.ForeignKey(Service, models.DO_NOTHING)

    class Meta:
        unique_together = (('cpe_port', 'service'),)

    def __str__(self):
        return self.cpe_port.cpe.serial_number + " - Port: " + self.cpe_port.name + \
        " - Service Id: " + str(self.service.pk)





