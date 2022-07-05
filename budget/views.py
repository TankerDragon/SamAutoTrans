from email import message
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from budget.models import Driver, Log, LogEdit, Group
from .forms import UserForm, DriverForm, LogForm
from django.contrib.auth.models import User
from .serializers import DriverSerializer
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
#funtions 
def get_name(id, arr):
    for a in arr:
        if id == a['id']:
            return a['first_name'] + ' ' + a['last_name']
    return '*name not found'
# Create your views here.
@login_required(login_url='login')
def main(request):
    # user = User.objects.get(username = request.user)
    if request.user.is_superuser:
        queryset = Driver.objects.all().order_by('first_name')
        l_total = 0
        d_total = 0
        r_total = 0
        s_total = 0
        for query in queryset:
            query.total_budget = query.d_budget + query.l_budget + query.r_budget + query.s_budget
            l_total += query.l_budget
            d_total += query.d_budget
            r_total += query.r_budget
            s_total += query.s_budget

        ##################
        data = {
            "week": {
                "D" : 0,
                "L" : 0,
                "R" : 0,
                "S" : 0,
                "T" : 0
            },
            "month": {
                "D" : 0,
                "L" : 0,
                "R" : 0,
                "S" : 0,
                "T" : 0
            },
            "year": {
                "D" : 0,
                "L" : 0,
                "R" : 0,
                "S" : 0,
                "T" : 0
            }
        }
        archives = Log.objects.filter(is_edited = False).order_by('date')
        today = datetime.datetime.today()
        week_before = today - datetime.timedelta(days = 7)
        month_before = today - datetime.timedelta(days = 30)
        year_before = today - datetime.timedelta(days = 365)
        #
        # week_before = datetime.datetime.strftime(today - datetime.timedelta(days = 7) , '%Y-%m-%d')  
        # month_before = datetime.datetime.strftime(today - datetime.timedelta(days = 30) , '%Y-%m-%d')
        # year_before = datetime.datetime.strftime(today - datetime.timedelta(days = 365) , '%Y-%m-%d')
        # print(week_before)
        # print(month_before)
        # print(year_before)
        # week_before2 = today - datetime.timedelta(days = 7)
        # print(week_before2)
        # w = filter(lambda a: a.date > week_before2, archives)
        # print(archives)
        # print(list(w))
        # for a in archives:
        #     print(a.date)
        week = list(filter(lambda a: a.date > week_before, archives))
        month = list(filter(lambda a: a.date > month_before, archives))
        year = list(filter(lambda a: a.date > year_before, archives))
        # week = archives.filter(date__gte = week_before)
        # month = archives.filter(date__gte = month_before)
        # year = archives.filter(date__gte = year_before)
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
            's_total': s_total,
            'total':l_total + d_total + r_total + s_total, 
            'is_superuser': request.user.is_superuser, 
            'user': request.user,
            'data': data
            }
        return render(request, 'budget.html', context)
    else:
        cloned_drivers_id = Group.objects.filter(staff_id = request.user.id)
        list_of_ids = []
        for i in cloned_drivers_id:
            list_of_ids.append(i.driver_id)
        queryset = Driver.objects.filter(id__in = list_of_ids).order_by('first_name')
        context = {
            'drivers': queryset, 
            'is_superuser': request.user.is_superuser, 
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
    log_edits = LogEdit.objects.all().values('edited_log')
    logEdits_list = list(map(lambda l: l['edited_log'], log_edits))
    # print(logEdits_list)
    #
    # user = User.objects.get(username = request.user)
    # drivers = Driver.objects.all()
    if request.user.is_superuser:
        queryset = Log.objects.all().filter(is_edited = False).order_by('-date')
    else:
        in_group = Group.objects.filter(staff = request.user)
        drivers_list = list(map(lambda l: l.driver_id, in_group))
        queryset = Log.objects.filter(driver_id__in = drivers_list, is_edited = False).order_by('-date')
    
    #preparing driver names
    driver_ids = list(map(lambda q: q.driver_id, queryset))
    driver_names = Driver.objects.filter(pk__in = driver_ids).values('id', 'first_name', 'last_name')

    for query in queryset:
        # driver = drivers.get(id = query.driver_id)
        query.name = get_name(query.driver_id, driver_names)
        query.edited_link = False
        # print(query.id)
        if query.id in logEdits_list:
            query.edited_link = True

    context = {'logs': queryset, 'is_superuser': request.user.is_superuser, 'user': request.user, 'many_drivers': True}
    return render(request, 'archive.html', context)

@login_required(login_url='login')
def driver_archive(request, id):
    log_edits = LogEdit.objects.all().values('edited_log')
    logEdits_list = list(map(lambda l: l['edited_log'], log_edits))
    #
    driver = Driver.objects.get(pk = id)

    if request.user.is_superuser:
        queryset = Log.objects.all().filter(driver_id = id, is_edited = False).order_by('-date')
    else:
        queryset = Log.objects.filter(driver_id = id, is_edited = False).filter(user = request.user).order_by('-date')

    for query in queryset:
        # driver = drivers.get(id = query.driver_id)
        # query.name = driver.first_name + ' ' + driver.last_name
        query.edited_link = False
        # print(query.id)
        if query.id in logEdits_list:
            query.edited_link = True

    context = {'logs': queryset, 'is_superuser': request.user.is_superuser, 'user': request.user, 'many_drivers': False, 'name': driver}
    return render(request, 'archive.html', context)


@login_required(login_url='login')
def archive_edits(request, id):
    pass



@login_required(login_url='login')
def edit_log(request, id):
    message = ""
    user = User.objects.get(username = request.user)
    log = Log.objects.get(pk = id)
    log_form = LogForm(instance=log)
    print(log_form.Meta.fields)
    if request.method == 'POST':
        data = request.POST
        #check if user selected its own driver
        in_group = Group.objects.filter(staff = user)
        drivers_list = list(map(lambda l: l.driver_id, in_group))
        print(drivers_list)
        print(data['driver'])
        print(type(data['driver']))
        if int(data['driver']) in drivers_list or user.is_superuser:
            log.is_edited = True
            log.save()
            #getting back changed budget from driver
            driver = Driver.objects.get(id = log.driver_id)
            if log.budget_type == 'D':
                driver.d_budget -= log.change
            elif log.budget_type == 'L':
                driver.l_budget -= log.change
            elif log.budget_type == 'R':
                driver.r_budget -= log.change
            elif log.budget_type == 'S':
                driver.s_budget -= log.change
            driver.save()
            #updating log
            new_log = Log()
            new_log.user = request.user
            new_log.driver_id = data['driver']
            new_log.change = Decimal(data['change'])
            new_log.budget_type = data['budget_type']
            new_log.bol_number = data['bol_number']
            new_log.pcs_number = data['pcs_number']
            new_log.note = data['note']
            new_log.save()

            #saving new changed budget to driver
            driver = Driver.objects.get(id = new_log.driver_id)
            if new_log.budget_type == 'D':
                driver.d_budget += new_log.change
            elif new_log.budget_type == 'L':
                driver.l_budget += new_log.change
            elif new_log.budget_type == 'R':
                driver.r_budget += new_log.change
            elif new_log.budget_type == 'S':
                driver.s_budget += new_log.change
            driver.save()
            # print(new_log.id)
            #saving log edition
            log_edit = LogEdit.objects.create(original_log = log, edited_log = new_log)
            log_edit.save()

            # print(request.POST)
            return redirect('archive')
        else:
            message = "you cant assign to this driver"

    context = {'form': log_form, 'is_superuser': user.is_superuser, 'user': user, 'message': message}
    return render(request, 'edit-log.html', context)


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
def reset(request, type):
    if request.user.is_superuser:
        #
        if type == 'D':
            query = Driver.objects.filter(~Q(d_budget = 0))
            for q in query:
                q.d_budget = 0
                q.save()
        elif type == 'L':
            query = Driver.objects.filter(~Q(l_budget = 0))
            for q in query:
                q.l_budget = 0
                q.save()
        elif type == 'R':
            query = Driver.objects.filter(~Q(r_budget = 0))
            for q in query:
                q.r_budget = 0
                q.save()
        elif type == 'S':
            query = Driver.objects.filter(~Q(s_budget = 0))
            for q in query:
                q.s_budget = 0
                q.save()
        else:
            return HttpResponse('there is no that type of budget')

        #
        logs = Log.objects.filter(budget_type = type)
        for log in logs:
            log.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return redirect('no-access')

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
            in_group = Group.objects.filter(staff = user)
            drivers_list = list(map(lambda l: l.driver_id, in_group))
            print(drivers_list)
            if user.is_superuser or driver.id in drivers_list:
                amount = Decimal(request.data['amount'])
                b_type = request.data['budget_type']
                if b_type == 'D':
                    driver.d_budget += amount
                elif b_type == 'L':
                    driver.l_budget += amount
                elif b_type == 'R':
                    driver.r_budget += amount
                elif b_type == 'S':
                    driver.s_budget += amount
                driver.save()
                log = Log(driver=driver, change = amount, budget_type=b_type, bol_number = request.data['bol_number'], pcs_number=request.data['pcs_number'], note=request.data['note'] ,user=request.user)
                log.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)