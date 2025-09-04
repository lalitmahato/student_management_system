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
from user.views import (
    CustomLoginView, logout_view, Error401View, PasswordReset, PasswordResetDone,
    PasswordResetConfirm, PasswordResetComplete, UserSignUpView, activate_account
)

app_name = 'user'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserSignUpView.as_view(), name='signup'),
    path('logout/', logout_view, name="logout"),
    path('unauthorized/', Error401View.as_view(), name='unauthorized'),
    path('forgot-password/', PasswordReset.as_view(), name="forgot_password"),
    path('reset-password/done/', PasswordResetDone.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('reset-password_complete/', PasswordResetComplete.as_view(),
         name="password_reset_complete"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    activate_account, name='account_activate'),
]
