from django.db import models

# Create your models here.
class Driver(models.Model):
    cdl_number = models.CharField(max_length=20, blank=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    co_driver_id = models.IntegerField(blank=True, null=True)
    app_version = models.CharField(max_length=5, blank=True)
    notes = models.CharField(max_length=255, blank=True)