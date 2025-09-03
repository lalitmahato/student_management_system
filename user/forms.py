from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import _unicode_ci_compare
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from core.settings import EMAIL_HOST_USER_FROM
from django.db.models import Q
from user.models import User
from user.tasks import send_password_reset_email

UserModel = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'phone_number', 'date_of_birth', 'gender', 'email',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = "form-control"
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['middle_name'].widget.attrs['class'] = "form-control"
        self.fields['middle_name'].widget.attrs['placeholder'] = "Middle Name"
        self.fields['last_name'].widget.attrs['class'] = "form-control"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
        self.fields['phone_number'].widget.attrs['class'] = "form-control"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['date_of_birth'].widget.attrs['class'] = "form-control"
        self.fields['gender'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['placeholder'] = "Email Address"
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = "Password"
        self.fields['password2'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm Password"

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1)
        except ValidationError as e:
            self.add_error('password1', e)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.is_active = False
            user.username = user.email
            user.save()
        return user


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User does not exist with this email.")
        return email

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
               and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
            self,
            domain_override=None,
            subject_template_name="registration/password_reset_subject.txt",
            email_template_name="registration/password_reset_email.html",
            use_https=False,
            token_generator=default_token_generator,
            from_email=None,
            request=None,
            html_email_template_name=None,
            extra_email_context=None,
    ):
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": {
                    'username': user.username,
                    'first_name': user.first_name,
                    'middle_name': user.middle_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'gender': user.gender,
                    'date_of_birth': user.date_of_birth,
                    'full_name': user.get_full_name()
                },
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            send_password_reset_email.apply_async(args=[
                subject_template_name,
                email_template_name,
                context,
                EMAIL_HOST_USER_FROM or from_email,
                user_email,
                html_email_template_name,
            ]
            )


class UserEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'phone_number', 'photo', 'date_of_birth', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = "form-control"
        self.fields['middle_name'].widget.attrs['class'] = "form-control"
        self.fields['last_name'].widget.attrs['class'] = "form-control"
        self.fields['phone_number'].widget.attrs['class'] = "form-control"
        self.fields['photo'].widget.attrs['class'] = "form-control"
        self.fields['date_of_birth'].widget.attrs['class'] = "form-control"
        self.fields['gender'].widget.attrs['class'] = "form-control"

        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['middle_name'].widget.attrs['placeholder'] = "Middle Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['date_of_birth'].widget.attrs['placeholder'] = "Date of Birth"
        self.fields['gender'].widget.attrs['placeholder'] = "Gender"
