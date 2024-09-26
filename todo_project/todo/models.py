from django.db import models
from .tasks import send_task_created_email

class Todo(models.Model):
    task_name = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_task_created_email.delay(self.task_name)

    def __str__(self):
        return self.task_name
