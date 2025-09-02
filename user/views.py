from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import resolve
from user.models import User
from user.decorators import unauthenticated_user

# Create your views here.

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        usr = User.objects.filter(email=email).first()
        if usr:
            user = authenticate(request, username=usr.username, password=password)
        else:
            user = None
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', None)
            if next_url:
                try:
                    current_url = resolve(next_url).app_name + ':' + resolve(next_url).url_name
                    return redirect(current_url)
                except:
                    return redirect('students:dashboard')
            return redirect('students:dashboard')
        elif usr:
            if not usr.is_active:
                messages.info(request, 'Your account is not active, kindly activate it')
            else:
                messages.info(request, "Username or Password is incorrect")
        else:
            messages.info(request, "Username or Password is incorrect")
    context = {
    }
    return render(request, "user/login.html", context)


@login_required(login_url='user:login')
def logout_view(request):
    logout(request)
    return redirect('user:login')


def error_401(request):
    return render(request, "401.html")