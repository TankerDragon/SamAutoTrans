from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='telesam'),
    path('get-new-id/', views.newID),
]