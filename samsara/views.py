from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
###
from .samsaraAPI import data, alarm
# Create your views here.
def main(request):
    return render(request, 'samsara.html')

def trailers(request):
    return render(request, 'trailers.html')

@api_view(['GET', 'POST'])
def get_data(request):
    if request.method == "GET":
        return Response({'data': data})
    elif request.method == "POST":
        print(request.data)
        alarm(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)