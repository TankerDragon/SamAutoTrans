from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from budget.models import Driver, Log
from .forms import CreateUserForm, DriverForm
from django.contrib.auth.models import User
from .serializers import DriverSerializer
from decimal import Decimal
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def main(request):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        queryset = Driver.objects.all().order_by('first_name')
    else:
        if user.user_type == 'D':
            queryset = Driver.objects.filter(dispatcher_id = user.id).order_by('first_name')
        elif user.user_type == 'U':
            queryset = Driver.objects.filter(updater_id = user.id).order_by('first_name')
    for query in queryset:
        query.total_budget = query.d_budget + query.l_budget + query.r_budget
    
    context = {'drivers': queryset, 'is_superuser': user.is_superuser, 'user': request.user}
    return render(request, 'budget.html', context)

@login_required(login_url='login')
def users(request):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        queryset = User.objects.filter(is_superuser = 0)
        context = {'users': queryset, 'is_superuser': user.is_superuser, 'user': request.user}
        return render(request, 'users.html', context)
    else:
        return redirect('no-access')

@login_required(login_url='login')
def new_user(request):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        user_form = CreateUserForm()
        if request.method == 'POST':
            user_form = CreateUserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('budget')

        context = {'form': user_form, 'is_superuser': user.is_superuser, 'user': request.user}
        return render(request, 'new-user.html', context)
    else:
        return redirect('no-access')

@login_required(login_url='login')
def new_driver(request):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        driver_form = DriverForm()
        if request.method == 'POST':
            driver_form = DriverForm(request.POST)
            if driver_form.is_valid():
                driver_form.save()
                return redirect('budget')

        context = {'form': driver_form, 'is_superuser': user.is_superuser, 'user': request.user}
        return render(request, 'driver.html', context)
    else:
        return redirect('no-access')

@login_required(login_url='login')
def driver_detail(request, id):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        driver = Driver.objects.get(pk=id)
        driver_form = DriverForm(instance=driver)
        if request.method == 'POST':
            driver_form = DriverForm(request.POST, instance=driver)
            if driver_form.is_valid():
                driver_form.save()
                return redirect('budget')

        context = {'form': driver_form, 'is_superuser': user.is_superuser, 'user': request.user}
        return render(request, 'driver.html', context)
    else:
        return redirect('no-access')


@login_required(login_url='login')
def archive(request):
    user = User.objects.get(username = request.user)
    drivers = Driver.objects.all()
    if user.is_superuser:
        queryset = Log.objects.all().order_by('-date')
    else:
        queryset = Log.objects.filter(user = user)

    for query in queryset:
        driver = drivers.get(id = query.driver_id)
        query.name = driver.first_name + ' ' + driver.last_name

    context = {'logs': queryset, 'is_superuser': user.is_superuser, 'user': request.user, 'many_drivers': True}
    return render(request, 'archive.html', context)

@login_required(login_url='login')
def driver_archive(request, id):
    user = User.objects.get(username = request.user)
    driver = Driver.objects.get(pk = id)

    if user.is_superuser:
        queryset = Log.objects.all().filter(driver_id = id).order_by('-date')
    else:
        queryset = Log.objects.filter(driver_id = id).filter(user = user).order_by('-date')

    for query in queryset:
        query.name = driver.first_name + ' ' + driver.last_name

    context = {'logs': queryset, 'is_superuser': user.is_superuser, 'user': request.user, 'many_drivers': False, 'name': driver.first_name + " " + driver.last_name}
    return render(request, 'archive.html', context)

@login_required(login_url='login')
@api_view(['GET', 'POST'])
def budget(request, id):
    # if request.method == 'GET':
    #     try:
    #         queryset = Driver.objects.get(pk = id)
    #         serializer = DriverSerializer(queryset)
    #         return Response(serializer.data)
    #     except Driver.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    user = User.objects.get(username = request.user)

    if request.method == 'POST':
        try:
            driver = Driver.objects.get(pk=id)
            if user.is_superuser or driver.dispatcher_id == user.id or driver.updater_id == user.id:
                if request.data['bol_number'] != '' and request.data['pcs_number'] != '':
                    amount = Decimal(request.data['amount'])
                    b_type = request.data['budget_type']
                    if b_type == 'D':
                        driver.d_budget += amount
                    elif b_type == 'L':
                        driver.l_budget += amount
                    elif b_type == 'R':
                        driver.r_budget += amount
                    driver.save()
                    log = Log(driver=driver, change = amount, budget_type=b_type, bol_number = request.data['bol_number'], pcs_number=request.data['pcs_number'], note=request.data['note'] ,user=request.user)
                    log.save()
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)