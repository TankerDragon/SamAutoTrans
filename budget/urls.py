from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='budget'),
    path('users/', views.users, name='users'),
    path('new-user/', views.new_user, name='new-user'),
    path('user-detail/<int:id>', views.user_detail),
    path('new-driver/', views.new_driver, name='new-driver'),
    path('driver-detail/<int:id>', views.driver_detail),
    path('archive/', views.archive, name='archive'),
    path('archive/<int:id>', views.driver_archive),
    path('deactivate-driver/<int:id>', views.deactivate_driver),
    path('activate-driver/<int:id>', views.activate_driver),
    path('<int:id>', views.budget)
]