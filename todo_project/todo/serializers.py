from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm Password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


class TodoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo  
        fields = ['id', 'task_name', 'is_done']


class TodoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo  
        fields = ['task_name', 'is_done']

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)


class TodoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['task_name', 'is_done']

    def update(self, instance, validated_data):
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.save()
        return instance
