from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    template_name = "students/dashboard.html"
    extra_context = {}
