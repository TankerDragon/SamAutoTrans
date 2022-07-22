from django.urls import path
from .views import getTrailers

urlpatterns = [
    path('', getTrailers)
]
