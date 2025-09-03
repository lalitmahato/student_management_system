import logging
from django.urls import resolve
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from user.decorators import unauthenticated_user
from user.forms import CustomPasswordResetForm


# Create your views here.
@method_decorator(unauthenticated_user, name='dispatch')
class CustomLoginView(LoginView):
    template_name = "user/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    default_redirect = 'students:dashboard'

    def get_success_url(self):
        # handle ?next= param safely
        next_url = self.request.GET.get('next')
        if next_url:
            try:
                current_url = resolve(next_url).app_name + ':' + resolve(next_url).url_name
                return redirect(current_url).url
            except Exception as e:
                logging.error("Error resolving next URL: %s", e)
                return redirect(self.default_redirect).url
        return redirect(self.default_redirect).url

    def form_invalid(self, form):
        user = form.get_user()
        if user and not user.is_active:
            messages.info(self.request, 'Your account is not active, kindly activate it')
        else:
            messages.info(self.request, "Username or Password is incorrect")
        return super().form_invalid(form)


@login_required(login_url='user:login')
def logout_view(request):
    logout(request)
    return redirect('user:login')


class PasswordReset(PasswordResetView):
    template_name = 'user/forget_password.html'
    email_template_name = 'email/password_reset_email_template.html'
    html_email_template_name = 'email/password_reset_email_template.html'
    success_url = reverse_lazy('user:password_reset_done')
    form_class = CustomPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'email/password_change_email_sent.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'user/reset_password.html'
    success_url = reverse_lazy('user:password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'user/password_reset_success.html'


class Error401View(TemplateView):
    template_name = "401.html"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("status", 401)
        return super().render_to_response(context, **response_kwargs)
