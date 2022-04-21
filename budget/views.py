from multiprocessing import context
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from budget.models import Driver
from .forms import CreateUserForm, DriverForm
from django.contrib.auth.models import User
from .serializers import DriverSerializer


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

@api_view(['GET', 'PATCH'])
def budget(request, id):
    if request.method == 'GET':
        try:
            queryset = Driver.objects.get(pk = id)
            serializer = DriverSerializer(queryset)
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PATCH':
        try:
            queryset = Driver.objects.get(pk =  id)
            serializer = DriverSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)