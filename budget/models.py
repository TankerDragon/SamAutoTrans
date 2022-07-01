from lib2to3.pgen2 import driver
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Staff(models.Model):
#     first_name = models.CharField(max_length=20, null=True)
#     last_name = models.CharField(max_length=20, null=True)
#     username = models.CharField(max_length=20, unique=True)
#     user_type = models.CharField(max_length=1, choices=[('D', 'dispatcher'), ('U', 'updater')], default='U')
#     password = models.CharField(max_length=12)
#     is_active = models.BooleanField(default=1)

class Driver(models.Model):
    d_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    l_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    r_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    s_budget = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, default=0)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    driver_type = models.CharField(max_length=2, choices=[('OO', 'Owner operator'), ('CD', 'Company driver'), ('LO', 'Lease operator')])
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Group(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

class Log(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    change = models.DecimalField(max_digits=9,decimal_places=2)
    budget_type = models.CharField(max_length=1, choices=[('D', 'driver'), ('L', 'lane'), ('R', 'recovery'), ('S', 'dirilis')])
    bol_number = models.CharField(max_length=15, blank=True)
    pcs_number = models.CharField(max_length=15, blank=True)
    user = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=100, blank=True)
    is_edited = models.BooleanField(default=False)

class LogEdit(models.Model):
    original_log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='original')
    edited_log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='edited')
    date = models.DateTimeField(auto_now=True)
