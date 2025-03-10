"""samauto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('home/', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('password-reset/', views.password_reset, name='password-reset'),
    path('budget/', include('budget.urls')),
    # path('trailers/', include('trailers.urls')),
    # path('eld/', include('eld.urls')),
    # path('samsara/', include('samsara.urls')),
    # path('telesam/', include('telesam.urls')),
    path('no-access/', views.noAccess, name='no-access'),
    path('__debug__/', include(debug_toolbar.urls))
]
