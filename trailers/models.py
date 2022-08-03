from django.db import models
from main.models import Driver
#choices
TRAILER_TYPE = (
    ('c', 'Company'),
    ('r', 'Ryder'),
    ('l', 'Lease'),
    ('o', 'Other'),
)
OPERATION = (
    (1, 'Hook'),
    (0, 'Drop')
)
# Create your models here.
    
class Trailer(models.Model):
    unit_number = models.CharField(max_length=12, unique=True)
    trailer_type = models.CharField(max_length=1, choices=TRAILER_TYPE, default='c')
    plate_number = models.CharField(max_length=15, unique=True)
    note = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=1)


class Log(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    other_driver = models.BooleanField(default=0)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)
    operation = models.BinaryField(choices=OPERATION, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    note = models.CharField(max_length=255, blank=True)