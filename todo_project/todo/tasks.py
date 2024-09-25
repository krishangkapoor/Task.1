from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_task_created_email(task_name):
    send_mail(
        'New Task Created',
        f'Task "{task_name}" has been created.',
        'krishangkapoor2004@gmail.com',
        ['krishangkapoor2004@gmail.com'],
        fail_silently=False,
    )
