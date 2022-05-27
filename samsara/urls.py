from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='samsara'),
    path('trailers/', views.trailers, name='trailers'),
    path('get-data/', views.get_data),
    path('get-trailers/', views.get_trailers),
]