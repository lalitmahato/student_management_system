"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('error-401/', error_401, name='error_401'),
    # path('forget/password/', forget_password, name='forget_password'),
    # path('user-password-reset/', user_password_reset_message, name='user_password_reset_message'),
    # path('user-registration/', user_registration_message, name='user_registration_message'),
    # path('user-dashboard/', user_dashboard, name='user_dashboard'),
    # path('reset/password/', reset_password, name='reset_password'),
]
