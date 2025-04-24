from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskAPITest(APITestCase):
    """Unit tests for Task CRUD + filtering."""

    def setUp(self):
        # two initial tasks
        Task.objects.create(title="T1", description="D1", date="2025-05-01")
        Task.objects.create(title="T2", description="D2", date="2025-06-01")

    def test_list_all(self):
        url = reverse('task-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_sort_by_date(self):
        url = reverse('task-list') + '?sort_by_date=true'
        res = self.client.get(url)
        dates = [t['date'] for t in res.data]
        self.assertEqual(dates, sorted(dates))

    def test_search_by_date(self):
        url = reverse('task-list') + '?search_date=2025-05-01'
        res = self.client.get(url)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['date'], '2025-05-01')

    def test_search_by_title(self):
        url = reverse('task-list') + '?search=T2'
        res = self.client.get(url)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'T2')

    def test_create_missing_field(self):
        url = reverse('task-list')
        res = self.client.post(url, {'title':'X'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_and_delete(self):
        task = Task.objects.first()
        detail = reverse('task-detail', args=[task.id])

        # PATCH
        res = self.client.patch(detail, {'description':'updated'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.description, 'updated')

        # DELETE
        res = self.client.delete(detail)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.id).exists())
