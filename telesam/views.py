from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'telesam.html')

def get_data(request):
    if request.method == "GET":
        return Response({'data': data, 'num': num})
    elif request.method == "POST":
        print(request.data)
        alarm(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def newID(request):
    return 0