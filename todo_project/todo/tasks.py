# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

# Token generator instance
token_generator = PasswordResetTokenGenerator()

@shared_task
def send_reset_email(email):
    """
    Send a password reset email to the user.
    """
    # Find the user associated with the email
    user = User.objects.filter(email=email).first()

    if user:
        # Generate token and create reset link
        uid = urlsafe_base64_encode(force_bytes(user.pk))  # Base64 encode the user's ID
        token = token_generator.make_token(user)  # Generate token for the user
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"  # Build reset link

        # Send email
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

@shared_task
def send_task_created_email(task_name, email):
    """
    Send an email notification when a new task is created.
    """
    send_mail(
        'New Task Created',
        f'A new task "{task_name}" has been created in your TODO list.',
        settings.DEFAULT_FROM_EMAIL,
        [email],  # Use the passed email
        fail_silently=False,
    )


