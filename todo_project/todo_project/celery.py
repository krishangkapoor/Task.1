from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')

django.setup()

app = Celery('todo_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)


