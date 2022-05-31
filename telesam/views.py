from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'telesam.html')