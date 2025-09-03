# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    template_name = "students/dashboard.html"
    extra_context = {}
