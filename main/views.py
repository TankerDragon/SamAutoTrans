from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PasswordResetForm
# Create your views here.
def main(request):
    return render(request, 'welcomepage.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def password_reset(request):
    user = User.objects.get(username=request.user)
    form = PasswordResetForm(instance=user)
    if request.method == 'POST':
            form = PasswordResetForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('budget')
    context = {
        'form' : form
    }

    return render(request, 'password-reset.html', context)

def noAccess(request):
    return render(request, 'no-access.html')