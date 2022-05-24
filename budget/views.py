from calendar import week
from re import L
from turtle import update
from django.shortcuts import render, redirect
from requests import request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from budget.models import Driver, Log, Group
from .forms import UserForm, DriverForm
from django.contrib.auth.models import User
from .serializers import DriverSerializer
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import datetime

#funtions 

# Create your views here.
@login_required(login_url='login')
def main(request):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        queryset = Driver.objects.all().order_by('first_name')
        l_total = 0
        d_total = 0
        r_total = 0
        for query in queryset:
            query.total_budget = query.d_budget + query.l_budget + query.r_budget
            l_total += query.l_budget
            d_total += query.d_budget
            r_total += query.r_budget

        ##################
        data = {
            "week": {
                "D" : 0,
                "L" : 0,
                "R" : 0,
                "T" : 0
            },
            "month": {
                "D" : 0,
                "L" : 0,
                "R" : 0,
                "T" : 0
            },
            "year": {
                "D" : 0,
                "L" : 0,
                "R" : 0,
                "T" : 0
            }
        }
        archives = Log.objects.all().order_by('date')
        today = datetime.datetime.today()
        week_before = datetime.datetime.strftime(today - datetime.timedelta(days = 7) , '%Y-%m-%d')  
        month_before = datetime.datetime.strftime(today - datetime.timedelta(days = 30) , '%Y-%m-%d')
        year_before = datetime.datetime.strftime(today - datetime.timedelta(days = 365) , '%Y-%m-%d')
        # print(week_before)
        # print(month_before)
        # print(year_before)

        week = archives.filter(date__gte = week_before)
        month = archives.filter(date__gte = month_before)
        year = archives.filter(date__gte = year_before)
        # print (week)

        for  i in week:
            data['week'][i.budget_type] += i.change
            data['week']['T'] += i.change
        for  i in month:
            data['month'][i.budget_type] += i.change
            data['month']['T'] += i.change
        for  i in year:
            data['year'][i.budget_type] += i.change
            data['year']['T'] += i.change
        

        context = {
            'drivers': queryset,
            'l_total': l_total,
            'd_total': d_total,
            'r_total': r_total,
            'total':l_total + d_total + r_total, 
            'is_superuser': user.is_superuser, 
            'user': request.user,
            'data': data
            }
        return render(request, 'budget.html', context)
    else:
        cloned_drivers_id = Group.objects.filter(staff_id = user.id)
        list_of_ids = []
        for i in cloned_drivers_id:
            list_of_ids.append(i.driver_id)
        queryset = Driver.objects.filter(id__in = list_of_ids).order_by('first_name')
        context = {
            'drivers': queryset, 
            'is_superuser': user.is_superuser, 
            'user': request.user,
            }
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
        user_form = UserForm()
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('budget')

        context = {'form': user_form, 'is_superuser': user.is_superuser, 'user': request.user}
        return render(request, 'new-user.html', context)
    else:
        return redirect('no-access')

@login_required(login_url='login')
def user_detail(request, id):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        u = User.objects.get(pk=id)
        user_form = UserForm(instance=u)
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=u)
            if user_form.is_valid():
                user_form.save()
                return redirect('budget')

        context = {
            'form': user_form, 
            'is_superuser': user.is_superuser, 
            'user': request.user
            }
        return render(request, 'user-detail.html', context)
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
        return render(request, 'new-driver.html', context)
    else:
        return redirect('no-access')

@login_required(login_url='login')
def driver_detail(request, id):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        users = User.objects.filter(is_superuser = 0)
        print('users', users)
        dispatchers = users.filter(user_type = 'D')
        updaters = users.filter(user_type = 'U')
        cloned_users_id = Group.objects.filter(driver_id = id)
        list_of_ids = []
        for i in cloned_users_id:
            list_of_ids.append(i.staff_id)

        cloned_users = users.filter(id__in = list_of_ids)
        
        driver = Driver.objects.get(pk=id)
        driver_form = DriverForm(instance=driver)
        if request.method == 'POST':
            dic = request.POST.dict()
            if dic['add_d'] != '':
                d = dispatchers.get(username = dic['add_d'])
                if cloned_users_id.filter(staff_id = d.id).exists():
                    print("exists")
                else:
                    new_g = Group()
                    new_g.driver_id = id
                    new_g.staff_id = d.id
                    new_g.save()
            if dic['add_u'] != '':
                u = updaters.get(username = dic['add_u'])
                if cloned_users_id.filter(staff_id = u.id).exists():
                    print("exists")
                else:
                    new_g = Group()
                    new_g.driver_id = id
                    new_g.staff_id = u.id
                    new_g.save()
            ####
            driver_form = DriverForm(request.POST, instance=driver)
            if driver_form.is_valid():
                driver_form.save()
                return redirect('budget')

        context = {
            'form': driver_form,
            'is_superuser': user.is_superuser, 
            'user': request.user, 
            'dispatchers': dispatchers,
            'updaters': updaters,
            'cloned_users': cloned_users
            }
        return render(request, 'driver-detail.html', context)
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
def deactivate_driver(request, id):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        driver = Driver.objects.get(pk = id)
        driver.is_active = 0
        driver.save()
    else:
        return redirect('no-access')
    return redirect('budget')

@login_required(login_url='login')
def activate_driver(request, id):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        driver = Driver.objects.get(pk = id)
        driver.is_active = 1
        driver.save()
    else:
        return redirect('no-access')
    return redirect('budget')




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