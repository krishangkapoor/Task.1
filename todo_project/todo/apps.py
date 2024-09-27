from django.apps import AppConfig

class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'

    def ready(self):
        from rest_framework import serializers
        if not hasattr(serializers, 'NullBooleanField'):
            serializers.NullBooleanField = serializers.BooleanField
