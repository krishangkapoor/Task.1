from rest_framework import viewsets
from .models import Todo
from .serializers import TodoReadSerializer, TodoWriteSerializer, TodoUpdateSerializer
from .tasks import send_task_created_email

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TodoReadSerializer  
        elif self.action == 'create':
            return TodoWriteSerializer  
        elif self.action == 'update' or self.action == 'partial_update':
            return TodoUpdateSerializer 
        return TodoReadSerializer  

    def perform_create(self, serializer):
        todo = serializer.save()  
        send_task_created_email.delay(todo.task_name)  
