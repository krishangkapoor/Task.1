# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

token_generator = PasswordResetTokenGenerator()

@shared_task
def send_reset_email(email):
    user = User.objects.filter(email=email).first()

    if user:
        uid = urlsafe_base64_encode(force_bytes(user.pk)) 
        token = token_generator.make_token(user)  
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/" 
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

@shared_task
def send_task_created_email(task_name, email):
    send_mail(
        'New Task Created',
        f'A new task "{task_name}" has been created in your TODO list.',
        settings.DEFAULT_FROM_EMAIL,
        [email],  
        fail_silently=False,
    )


