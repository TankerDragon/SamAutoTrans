from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='budget'),
    path('users/', views.users, name='users'),
    path('new-user/', views.new_user, name='new-user'),
    path('new-driver/', views.new_driver, name='new-driver')
]