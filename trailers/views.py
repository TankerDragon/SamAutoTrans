from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Trailer
from .serializers import TrailerSerializer

# Create your views here.
# def trailers(request):
#     queryset = Trailer.objects.all()

#     context = {
#         'trailers' : queryset,
#         'category' : 'trailers'
#     }
#     return render(request, "trailers.html", context)

@api_view(['GET', 'POST'])
def trailers(request):
    if request.method == 'GET':
        queryset = Trailer.objects.all()
        serializer = TrailerSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TrailerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'PUT':
    #     log_id = request.data['id']
    #     query = Log.objects.filter(driver_id_id=id).get(pk=log_id)
    #     serializer = LogSerializer(query, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response('updated')

