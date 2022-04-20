from multiprocessing import context
from django.shortcuts import render, redirect

from budget.models import Driver
from .forms import CreateUserForm, DriverForm
from django.contrib.auth.models import User


# class number:
#     value = 0
#     def get(self):
#         return self.value
    
#     def increase(self):
#         self.value += 1

# n = number()
# Create your views here.
def main(request):
    queryset = Driver.objects.all()
    context = {'drivers': queryset}
    return render(request, 'budget.html', context)

def users(request):
    queryset = User.objects.filter(is_superuser = 0)
    context = {'users': queryset}
    return render(request, 'users.html', context)

def new_user(request):
    user_form = CreateUserForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('budget')

    context = {'form': user_form}
    return render(request, 'new-user.html', context)

def new_driver(request):
    driver_form = DriverForm()
    if request.method == 'POST':
        driver_form = DriverForm(request.POST)
        if driver_form.is_valid():
            driver_form.save()
            return redirect('budget')

    context = {'form': driver_form}
    return render(request, 'new-driver.html', context)