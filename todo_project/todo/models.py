from django.db import models
from django.contrib.auth.models import User  
from .tasks import send_task_created_email

class Todo(models.Model):
    task_name = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
   
    def save(self, *args, **kwargs):
        """
        Save the TODO instance and send a task creation email notification asynchronously.
        """
        super().save(*args, **kwargs)
        # Send an email notification when a task is created, passing the user's email
        send_task_created_email.delay(self.task_name, self.user.email)

    def __str__(self):
        return self.task_name
