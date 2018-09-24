from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Client(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=50, unique=True)

####### To be deleted ######
    bandwidth = models.PositiveSmallIntegerField(blank=True, null=True)
    vrf_name = models.CharField(max_length=50, blank=True)
    prefix = models.CharField(max_length=50, blank=True)
    client_network = models.CharField(max_length=50, blank=True)
    wan_ip = models.CharField(max_length=50, blank=True) #TODO move to client node on inventory and wrap
    access_node = models.CharField(max_length=50, blank=True)
    access_node_port = models.CharField(max_length=50, blank=True)
    client_node_sn = models.CharField(max_length=50, blank=True)
    client_node_port = models.CharField(max_length=50, blank=True)
    autonomous_system = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(65000),MaxValueValidator(65500)])
    location = models.CharField(max_length=30, blank=True)

    SERVICE_STATE_CHOICES = (
    ("PENDING", "PENDING"),
    ("REQUESTED", "REQUESTED"),
    ("COMPLETED", "COMPLETED"),
    ("ERROR", "ERROR")
    )
    service_state = models.CharField(max_length=15,
                  choices=SERVICE_STATE_CHOICES,
                  default="PENDING")
####### End of To be deleted ######

    service_type = models.CharField(max_length=30)


    def __str__(self):
        return "SERVICE_ID: " + str(self.pk)



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



