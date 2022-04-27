from lib2to3.pgen2 import driver
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

    def __str__(self):
        return self.first_name

class Log(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    change = models.DecimalField(max_digits=9,decimal_places=2)
    budget_type = models.CharField(max_length=1, choices=[('D', 'driver'), ('L', 'lane'), ('R', 'recovery')])
    bol_number = models.CharField(max_length=15)
    pcs_number = models.CharField(max_length=15)
    user = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)