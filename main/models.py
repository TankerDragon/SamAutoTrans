from django.db import models

#choices
DRIVER_TYPE = (
    ('OO', 'Owner operator'), 
    ('CD', 'Company driver'), 
    ('LO', 'Lease operator')
)
# Create your models here.
class Driver(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    driver_type = models.CharField(max_length=2, choices=DRIVER_TYPE)
    # cdl_number = models.CharField(max_length=20, blank=True)
    # vehicle_id = models.IntegerField(blank=True, null=True)
    # co_driver_id = models.IntegerField(blank=True, null=True)
    # app_version = models.CharField(max_length=5, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.first_name + ' ' + self.last_name