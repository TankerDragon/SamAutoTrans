from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='budget'),
    path('new-user/', views.new_user, name='new-user'),
    path('users/', views.users, name='users')
]