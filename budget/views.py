import re
from django.shortcuts import render

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
    return render(request, 'budget.html', {'num': num})