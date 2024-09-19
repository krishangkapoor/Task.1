from django.urls import path
from .views import TodoListCreate, TodoUpdate, TodoDelete

urlpatterns = [
    path('todo/list/', TodoListCreate.as_view(), name='todo-list-create'),
    path('todo/update/<int:pk>/', TodoUpdate.as_view(), name='todo-update'),
    path('todo/delete/<int:pk>/', TodoDelete.as_view(), name='todo-delete'),
]
