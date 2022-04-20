from multiprocessing import context
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User


class number:
    value = 0
    def get(self):
        return self.value
    
    def increase(self):
        self.value += 1

n = number()
# Create your views here.
def main(request):
    n.increase()
    num = n.get()
    #

    return render(request, 'budget.html', {'num': num})

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