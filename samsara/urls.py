from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='samsara'),
    path('get-data/', views.get_data),
]