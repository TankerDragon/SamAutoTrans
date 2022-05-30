from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
###
from .samsaraAPI import data, trailers_data, alarm, trailer_alarm, num
# Create your views here.
def main(request):
    return render(request, 'samsara.html')

def trailers(request):
    return render(request, 'trailers.html')

@api_view(['GET', 'POST'])
def get_data(request):
    if request.method == "GET":
        return Response({'data': data, 'num': num})
    elif request.method == "POST":
        print(request.data)
        alarm(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_trailers(request):
    if request.method == "GET":
        return Response({'trailers': trailers_data, 'num': num})
    elif request.method == "POST":
        print(request.data)
        trailer_alarm(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)