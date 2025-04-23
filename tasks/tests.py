from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Task

class TaskTests(APITestCase):
    def test_create_task(self):
        url = reverse('task-list')
        data = {'title': 'Test', 'description': 'Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
