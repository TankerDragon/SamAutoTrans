# from attr import field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Driver, Log

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name',
                  'last_name','user_type','is_active', 'password1', 'password2']



class DriverForm(ModelForm):
    class Meta:
        model = Driver
        # ['user_id', 'cdl_number', 'vehicle_id', 'notes']
        fields = '__all__'

class LogForm(ModelForm):
    class Meta:
        model  = Log
        fields = ['driver', 'change', 'budget_type', 'bol_number', 'pcs_number', 'note']




# class AmountChangeForm(ModelForm):
#     your_name = forms.CharField(label='Your name', max_length=100)
