from django.db import models

# {'id': '281474979402267', 'name': 'Unit-000459', 'gps': [{'decorations': {'obdOdometerMeters': {'value': 1004633180}}, 'time': '2022-05-25T15:13:41.999Z', 'latitude': 41.24579395, 'longitude': -81.24902857, 'headingDegrees': 273.9, 'speedMilesPerHour': 71.463, 'reverseGeo': {'formattedLocation': 'Ohio Turnpike, Freedom Township, OH, 44288'}, 'isEcuSpeed': True}]}

# Create your models here.
class Log(models.Model):
    samsara_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50, null=True)
    odometer = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    headingDegrees = models.SmallIntegerField(null=True)
    speed = models.SmallIntegerField(null=True)
    location = models.CharField(max_length=120, null=True)

