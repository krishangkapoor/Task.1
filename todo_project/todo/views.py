from django.shortcuts import render
from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer

# List and Create tasks
class TodoListCreate(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        # Optionally filter by completion status
        is_done = self.request.query_params.get('is_done')
        if is_done is not None:
            return Todo.objects.filter(is_done=is_done)
        return super().get_queryset()

# Update task (mark as done)
class TodoUpdate(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

# Delete task
class TodoDelete(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

