from django.contrib import admin
from .models import Todo  

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'is_done')  
    list_filter = ('is_done',)  
    search_fields = ('task_name',)  