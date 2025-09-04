import logging

from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.shortcuts import redirect
from django.urls import resolve
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView, CreateView

from user.decorators import unauthenticated_user
from user.forms import CustomPasswordResetForm, UserRegistrationForm
from user.models import User
from user.token import account_activation_token


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


class UserSignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("user:login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


@login_required(login_url='user:login')
def logout_view(request):
    logout(request)
    return redirect('students:index_page')


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


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email. You can now log in to your account.')
        return redirect('user:login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('user:login')
