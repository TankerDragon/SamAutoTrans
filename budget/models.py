from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Driver(models.Model):
    dispatcher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dispatcher', blank=True)
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updater', blank=True)
    d_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    l_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    r_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=1)