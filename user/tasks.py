from celery import shared_task
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, EmailMessage

from core.settings import EMAIL_HOST_USER_FROM
from user.models import User
from user.token import account_activation_token

@shared_task
def send_account_activation_email(user_id, protocol='http', domain="localhost:8000"):
    user = User.objects.filter(id=user_id).first()
    if user:
        mail_subject = 'Activate Your Account Now! (Student Management System)'
        body_message = render_to_string('email/account_activation_email.html', {
            'protocol': protocol,
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        from_email = EMAIL_HOST_USER_FROM
        email = EmailMessage(mail_subject, body_message, to=[to_email], from_email=from_email)
        email.content_subtype = "html"
        email.send()

@shared_task
def send_password_reset_email(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
    """Send a django.core.mail.EmailMultiAlternatives to `to_email`."""
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()



@shared_task
def send_email_message(mail_subject, message, to):
    email = EmailMessage(mail_subject, message, to=[to], from_email=EMAIL_HOST_USER_FROM)
    email.content_subtype = "html"
    email.send()
