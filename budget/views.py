from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from budget.models import Driver, Log, LogEdit
from .forms import UserForm, DriverForm, LogForm
from django.contrib.auth.models import User
from .serializers import DriverSerializer, LogSerializer
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#funtions 
def get_week_start():
    now = datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=1)
    days = WEEKDAYS.index(now.strftime("%A")) + 1  # starting date from Saturday
    week_start = now - datetime.timedelta(days=days)
    return week_start

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
        # data = {
        #     "week": {
        #         "D" : 0,
        #         "L" : 0,
        #         "R" : 0,
        #         "S" : 0,
        #         "T" : 0
        #     },
        #     "month": {
        #         "D" : 0,
        #         "L" : 0,
        #         "R" : 0,
        #         "S" : 0,
        #         "T" : 0
        #     },
        #     "year": {
        #         "D" : 0,
        #         "L" : 0,
        #         "R" : 0,
        #         "S" : 0,
        #         "T" : 0
        #     }
        # }
        # archives = Log.objects.filter(is_edited = False).order_by('date')
        # today = datetime.datetime.today()
        # week_before = today - datetime.timedelta(days = 7)
        # month_before = today - datetime.timedelta(days = 30)
        # year_before = today - datetime.timedelta(days = 365)
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
        ## week = list(filter(lambda a: a.date > week_before, archives))
        ## month = list(filter(lambda a: a.date > month_before, archives))
        ## year = list(filter(lambda a: a.date > year_before, archives))
        # week = archives.filter(date__gte = week_before)
        # month = archives.filter(date__gte = month_before)
        # year = archives.filter(date__gte = year_before)
        # print (week)

        # for  i in week:
        #     data['week'][i.budget_type] += i.change
        #     data['week']['T'] += i.change
        # for  i in month:
        #     data['month'][i.budget_type] += i.change
        #     data['month']['T'] += i.change
        # for  i in year:
        #     data['year'][i.budget_type] += i.change
        #     data['year']['T'] += i.change
        
        usersList = User.objects.filter(is_superuser = 0).values('username')


        context = {
            'usersList': usersList,
            'drivers': queryset,
            'l_total': l_total,
            'd_total': d_total,
            'r_total': r_total,
            's_total': s_total,
            'total':l_total + d_total + r_total + s_total, 
            'is_superuser': request.user.is_superuser, 
            'user': request.user,
            'category' : 'budget'
            }
        return render(request, 'budget.html', context)
    else:
        # cloned_drivers_id = Group.objects.filter(staff_id = request.user.id)
        # list_of_ids = []
        # for i in cloned_drivers_id:
        #     list_of_ids.append(i.driver_id)
        queryset = Driver.objects.filter(dispatcher=request.user).order_by('first_name')
        context = {
            'drivers': queryset, 
            'is_superuser': request.user.is_superuser, 
            'user': request.user,
            'category' : 'budget'
            }
        return render(request, 'budget.html', context)


@login_required(login_url='login')
@api_view(['POST'])
def getInDates(request):
    data = {
        "message": "",
        "D" : 0,
        "L" : 0,
        "R" : 0,
        "S" : 0,
        "T" : 0
    }
    # print(request.data)
    if request.data['start_date'] and request.data['end_date']:
        start_date = datetime.datetime.strptime(request.data['start_date'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(request.data['end_date'], '%Y-%m-%d') + datetime.timedelta(days=1)
        if request.data['user']:
            archives = Log.objects.filter(is_edited = False, user = request.data['user']).filter(date__gte = start_date, date__lte = end_date)
            data['message'] = "from " + request.data['start_date'] + " to " + request.data['end_date'] + " by " + request.data['user']
        else:
            archives = Log.objects.filter(is_edited = False).filter(date__gte = start_date, date__lte = end_date)
            data['message'] = "from " + request.data['start_date'] + " to " + request.data['end_date']
        # print(data)
        for a in archives:
            data[a.budget_type] += a.change
            data["T"] += a.change

        return Response(data)
    data['message'] = "*** Date is not selected! ***"
    return Response(data)

@login_required(login_url='login')
def users(request):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        queryset = User.objects.filter(is_superuser = 0)
        context = {'users': queryset, 'is_superuser': user.is_superuser, 'user': request.user, 'category' : 'all-dispatchers'}
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

        context = {'form': user_form, 'is_superuser': user.is_superuser, 'user': request.user, 'category' : 'add-dispatcher'}
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

        context = {'form': driver_form, 'is_superuser': user.is_superuser, 'user': request.user, 'category' : 'add-driver'}
        return render(request, 'new-driver.html', context)
    else:
        return redirect('no-access')

@login_required(login_url='login')
def driver_detail(request, id):
    user = User.objects.get(username = request.user)
    if user.is_superuser:
        # users = User.objects.filter(is_superuser = 0)
        # print('users', users)
        # dispatchers = users.filter(user_type = 'D')
        # updaters = users.filter(user_type = 'U')
        # cloned_users_id = Group.objects.filter(driver_id = id)
        # list_of_ids = []
        # for i in cloned_users_id:
        #     list_of_ids.append(i.staff_id)

        # cloned_users = users.filter(id__in = list_of_ids)
        
        driver = Driver.objects.get(pk=id)
        driver_form = DriverForm(instance=driver)
        if request.method == 'POST':
            # dic = request.POST.dict()
            # if dic['add_d'] != '':
            #     d = dispatchers.get(username = dic['add_d'])
            #     if cloned_users_id.filter(staff_id = d.id).exists():
            #         print("exists")
            #     else:
            #         new_g = Group()
            #         new_g.driver_id = id
            #         new_g.staff_id = d.id
            #         new_g.save()
            # if dic['add_u'] != '':
            #     u = updaters.get(username = dic['add_u'])
            #     if cloned_users_id.filter(staff_id = u.id).exists():
            #         print("exists")
            #     else:
            #         new_g = Group()
            #         new_g.driver_id = id
            #         new_g.staff_id = u.id
            #         new_g.save()
            ####
            driver_form = DriverForm(request.POST, instance=driver)
            if driver_form.is_valid():
                driver_form.save()
                return redirect('budget')

        context = {
            'form': driver_form,
            'is_superuser': user.is_superuser, 
            'user': request.user
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
        queryset = Log.objects.filter(is_edited = False).order_by('-date')
    else:
        # in_group = Group.objects.filter(staff = request.user)
        # drivers_list = list(map(lambda l: l.driver_id, in_group))
        drivers = Driver.objects.filter(dispatcher = request.user).values('id')
        driverIDs = [d['id'] for d in drivers]
        queryset = Log.objects.filter(driver_id__in = driverIDs, is_edited = False).order_by('-date')
        
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

    context = {'logs': queryset, 'is_superuser': request.user.is_superuser, 'user': request.user, 'many_drivers': True, 'category' : 'archive'}
    return render(request, 'archive.html', context)

@login_required(login_url='login')
def archiveBetweenDates(request, startDate, endDate):
    start_date = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(endDate, '%Y-%m-%d') + datetime.timedelta(days=1)

    log_edits = LogEdit.objects.all().values('edited_log')
    logEdits_list = list(map(lambda l: l['edited_log'], log_edits))
    # print(logEdits_list)
    #
    # user = User.objects.get(username = request.user)
    # drivers = Driver.objects.all()
    if request.user.is_superuser:
        queryset = Log.objects.all().filter(is_edited = False, date__gte = start_date, date__lte = end_date).order_by('-date')
    else:
        # in_group = Group.objects.filter(staff = request.user)
        # drivers_list = list(map(lambda l: l.driver_id, in_group))
        queryset = Log.objects.filter(user=request.user, is_edited = False, date__gte = start_date, date__lte = end_date).order_by('-date') #, user=request.user
    
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

    context = {'logs': queryset, 'is_superuser': request.user.is_superuser, 'user': request.user, 'many_drivers': True, 'category' : 'archive'}
    return render(request, 'archive.html', context)

@login_required(login_url='login')
def archiveBetweenDatesBy(request, id, startDate, endDate):

    start_date = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(endDate, '%Y-%m-%d') + datetime.timedelta(days=1)

    log_edits = LogEdit.objects.all().values('edited_log')
    logEdits_list = list(map(lambda l: l['edited_log'], log_edits))
    #
    driver = Driver.objects.get(pk = id)

    if request.user.is_superuser:
        queryset = Log.objects.all().filter(driver_id = id, is_edited = False,  date__gte = start_date, date__lte = end_date).order_by('-date')
    else:
        # in_group = Group.objects.filter(staff = request.user)
        # drivers_list = list(map(lambda l: l.driver_id, in_group))
        queryset = Log.objects.filter(user =request.user, is_edited = False,  date__gte = start_date, date__lte = end_date).order_by('-date') #, user=request.user

    for query in queryset:
        # driver = drivers.get(id = query.driver_id)
        # query.name = driver.first_name + ' ' + driver.last_name
        query.edited_link = False
        # print(query.id)
        if query.id in logEdits_list:
            query.edited_link = True

    context = {'logs': queryset, 'is_superuser': request.user.is_superuser, 'user': request.user, 'many_drivers': False, 'name': driver, 'category' : 'archive'}
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
        # in_group = Group.objects.filter(staff = request.user)
        # drivers_list = list(map(lambda l: l.driver_id, in_group))
        queryset = Log.objects.filter(driver_id = id, is_edited = False).order_by('-date') #, user=request.user

    for query in queryset:
        # driver = drivers.get(id = query.driver_id)
        # query.name = driver.first_name + ' ' + driver.last_name
        query.edited_link = False
        # print(query.id)
        if query.id in logEdits_list:
            query.edited_link = True

    context = {'logs': queryset, 'is_superuser': request.user.is_superuser, 'user': request.user, 'many_drivers': False, 'name': driver, 'category' : 'archive'}
    return render(request, 'archive.html', context)


@login_required(login_url='login')
def archive_edits(request, id):
    #selecting logs only related to given ID
    editGroup = LogEdit.objects.all().order_by('-date') #values('original_log', 'edited_log')
    nextPickID = id
    pickedLogs = []
    pickedLogs.append(id)
    for g in editGroup:
        if g.edited_log_id == nextPickID:
            nextPickID = g.original_log_id
            pickedLogs.append(nextPickID)
    editedLogs = Log.objects.filter(pk__in = pickedLogs).order_by('-date')
    #adding drivers name
    driver_ids = list(map(lambda q: q.driver_id, editedLogs))
    driver_names = Driver.objects.filter(pk__in = driver_ids).values('id', 'first_name', 'last_name')
    for e_query in editedLogs:
        e_query.name = get_name(e_query.driver_id, driver_names)

    context = {'logs': editedLogs, 'is_superuser': request.user.is_superuser, 'user': request.user, 'category' : 'archive'}
    return render(request, 'edited-archive.html', context)



@login_required(login_url='login')
def edit_log(request, id):
    message = ""
    user = User.objects.get(username = request.user)
    log = Log.objects.get(pk = id)
    log_form = LogForm(instance=log)
    if request.method == 'POST':
        data = request.POST
        #check if user selected its own driver
        check_driver = Driver.objects.get(pk = int(data['driver']))
        # in_group = Group.objects.filter(staff = user)
        # drivers_list = list(map(lambda l: l.driver_id, in_group))
        #check pcs number
        check_pcs = Log.objects.filter(pcs_number=data['pcs_number'], is_edited=False).values('pcs_number')
        if check_pcs and log.pcs_number != data['pcs_number']:
            return redirect('/budget/edit-log/' + str(id))

        if check_driver.dispatcher == request.user or user.is_superuser:
            log.is_edited = True
            created_time = log.date
            log.save()
            driver = Driver.objects.get(id = log.driver_id)
            #getting back changed budget from driver
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
            change_new_log = Decimal(data['original_rate']) - Decimal(data['current_rate'])
            new_log = Log()
            new_log.user = request.user
            new_log.driver_id = data['driver']
            new_log.original_rate = Decimal(data['original_rate'])
            new_log.current_rate = Decimal(data['current_rate'])
            new_log.change = change_new_log
            new_log.total_miles = data['total_miles']
            new_log.budget_type = data['budget_type']
            new_log.bol_number = data['bol_number']
            new_log.pcs_number = data['pcs_number']
            new_log.note = data['note']
            new_log.date = created_time
            saved_log = new_log.save()
            # saved_log.date = created_time
            # saved_log.save()

            #saving new changed budget to driver
            driver = Driver.objects.get(id = new_log.driver_id)
            if new_log.budget_type == 'D':
                driver.d_budget += change_new_log
            elif new_log.budget_type == 'L':
                driver.l_budget += change_new_log
            elif new_log.budget_type == 'R':
                driver.r_budget += change_new_log
            elif new_log.budget_type == 'S':
                driver.s_budget += change_new_log
            driver.save()
            # print(new_log.id)
            #saving log edition
            log_edit = LogEdit.objects.create(original_log = log, edited_log = new_log)
            log_edit.save()

            # print(request.POST)
            return redirect('archive')
        else:
            message = "you cant assign to this driver"

    context = {'form': log_form, 'is_superuser': user.is_superuser, 'user': user, 'message': message, 'category' : 'archive'}
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

ENABLE_RESET = False

@login_required(login_url='login')
@api_view(['GET', 'POST'])
def reset(request, type):
    if not ENABLE_RESET:
        return HttpResponse('action temporarily not available')

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

    if request.method == 'POST':
        driver = Driver.objects.get(pk=id)
        #print(request.data)
        # in_group = Group.objects.filter(staff = request.user)
        # drivers_list = list(map(lambda l: l.driver_id, in_group))
        # print(drivers_list)
        if request.user.is_superuser or driver.dispatcher == request.user:
            data = request.data
            print(type(request.data['total_miles']))
            check_pcs = Log.objects.filter(pcs_number=request.data['pcs_number'], is_edited=False).values('pcs_number')
            if request.data['original_rate'] == '' or request.data['current_rate'] == '' or check_pcs:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            #print(request.data)
            change = Decimal(request.data['original_rate']) - Decimal(request.data['current_rate'])
            b_type = request.data['budget_type']
            data['driver'] = id
            data['user'] = str(request.user)
            data['change'] = change
            #data['total_miles'] = int(float(data['total_miles']))
            # now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # print(now)
            # data['date'] = now
            log = LogSerializer(data=data)
            if log.is_valid():
                saved_log = log.save()
                saved_log.date = datetime.datetime.now()
                saved_log.save()
                #print(saved_log.id)
                if b_type == 'D':
                    driver.d_budget += change
                elif b_type == 'L':
                    driver.l_budget += change
                elif b_type == 'R':
                    driver.r_budget += change
                elif b_type == 'S':
                    driver.s_budget += change
                driver.save()
            else:
                print(log.errors)
                return Response(log.errors, status=status.HTTP_400_BAD_REQUEST)


            # original_rate = Decimal(request.data['original_rate'])
            # current_rate = Decimal(request.data['current_rate'])
            # amount = original_rate - current_rate
            # b_type = request.data['budget_type']
            # total_miles = request.data['total_miles']
           
            # log = Log(driver=driver, original_rate = original_rate, current_rate = current_rate, change = amount, total_miles=total_miles, budget_type=b_type, bol_number = request.data['bol_number'], pcs_number=request.data['pcs_number'], note=request.data['note'] ,user=request.user)
            # log.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required(login_url='login')
def drivers_board(request, week_before):
    week_start = get_week_start() - datetime.timedelta(days=(7 * week_before))
    week_end = week_start + datetime.timedelta(days=6)
    # till_today = datetime.datetime.now() + datetime.timedelta(days=1)

    dispatchers = User.objects.all()
    dispatchers_list = list(map(lambda d: [d.id, d.username], dispatchers))
    logs = Log.objects.filter(date__gte = week_start, date__lte = week_end + datetime.timedelta(days=1), is_edited=False)

    if request.user.is_superuser:
        drivers = Driver.objects.all().order_by('first_name')
        # print((drivers[0]))
        # print((logs[0]))
    else:
        drivers = Driver.objects.filter(dispatcher=request.user).order_by('first_name')

    for driver in drivers:
        driver.disp =''
        for d in dispatchers_list:
            if driver.dispatcher_id == d[0]:
                driver.disp = d[1]

        driver_logs = list(filter(lambda l: l.driver_id == driver.id, logs))
        total_miles = 0
        actual_gross = 0
        for l in driver_logs:
            total_miles += l.total_miles
            actual_gross += l.current_rate

        driver.loads = len(driver_logs)
        driver.total_miles = total_miles
        driver.actual_gross = actual_gross
        if total_miles == 0:
            driver.rate = 0
        else:    
            driver.rate = round((actual_gross / total_miles)*100) / 100

        if driver.gross_target == 0:
            driver.percentage = 0
        else:    
            driver.percentage = round((actual_gross / driver.gross_target) * 10000) / 100

    drivers = sorted(drivers, key=lambda d: d.percentage, reverse=True)

    context = {
        'drivers': drivers, 
        'is_superuser': request.user.is_superuser, 
        'user': request.user,
        'category' : 'drivers-gross',
        "week_start": week_start.date,
        "week_end": week_end.date
        }
    return render(request, "drivers-board.html", context)


@login_required(login_url='login')
def dispatchers_board(request, week_before):
    week_start = get_week_start() - datetime.timedelta(days=(7 * week_before))
    week_end = week_start + datetime.timedelta(days=6)
    # till_today = datetime.datetime.now() + datetime.timedelta(days=1)

    dispatchers = User.objects.filter(is_superuser=False)
    dispatchers_list = list(map(lambda d: [d.id, d.username], dispatchers))
    logs = Log.objects.filter(date__gte = week_start, date__lte = week_end + datetime.timedelta(days=1), is_edited=False)

    
    drivers = Driver.objects.all()

    for driver in drivers:

        driver_logs = list(filter(lambda l: l.driver_id == driver.id, logs))
        total_miles = 0
        actual_gross = 0
        for l in driver_logs:
            total_miles += l.total_miles
            actual_gross += l.current_rate

        driver.total_miles = total_miles
        driver.actual_gross = actual_gross
        # if total_miles == 0:
        #     driver.rate = 0
        # else:    
        #     driver.rate = round((actual_gross / total_miles)*100) / 100

        # if driver.gross_target == 0:
        #     driver.percentage = 0
        # else:    
        #     driver.percentage = (actual_gross / driver.gross_target) * 100
    
    for dispatcher in dispatchers:
        dispatcher_drivers = list(filter(lambda d: d.dispatcher_id == dispatcher.id, drivers))
        total_miles = 0
        actual_gross = 0
        target_gross = 0
        for d in dispatcher_drivers:
            total_miles += d.total_miles
            actual_gross += d.actual_gross
            target_gross += d.gross_target
        
        dispatcher.drivers = len(dispatcher_drivers)
        dispatcher.total_miles = total_miles
        dispatcher.actual_gross = actual_gross
        dispatcher.target_gross = target_gross


        if total_miles == 0:
            dispatcher.rate = 0
        else:    
            dispatcher.rate = round((actual_gross / total_miles)*100) / 100

        if target_gross == 0:
            dispatcher.percentage = 0
        else:    
            dispatcher.percentage = round((actual_gross / target_gross) * 10000) / 100
        
    
    dispatchers = sorted(dispatchers, key=lambda d: d.percentage, reverse=True)


    context = {
        'dispatchers': dispatchers, 
        'is_superuser': request.user.is_superuser, 
        'user': request.user,
        'category' : 'dispatchers-gross',
        "week_start": week_start.date,
        "week_end": week_end.date
        }
    return render(request, "dispatchers-board.html", context)
