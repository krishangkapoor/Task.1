from rest_framework import serializers
from .models import Todo

class TodoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'task_name', 'is_done']  

class TodoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['task_name']  

class TodoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['task_name', 'is_done']  
