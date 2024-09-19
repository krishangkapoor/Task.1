from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Todo

class TodoAPITests(APITestCase):
    def test_create_task(self):
        url = reverse('todo-list-create')
        data = {'task_name': 'Test Task'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_tasks(self):
        Todo.objects.create(task_name="Test Task", is_done=False)
        url = reverse('todo-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        task = Todo.objects.create(task_name="Test Task", is_done=False)
        url = reverse('todo-update', args=[task.id])
        data = {'is_done': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_task(self):
        task = Todo.objects.create(task_name="Test Task", is_done=False)
        url = reverse('todo-delete', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

