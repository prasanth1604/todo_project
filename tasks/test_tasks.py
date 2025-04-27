from django.test import TestCase
import pytest
from django.utils import timezone
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from rest_framework.request import Request
from tasks.models import Task
from tasks.services.task_filter_service import TaskFilterService

# Create your tests here.

# -------------------------------
# Unit Tests for TaskFilterService
# -------------------------------
@pytest.mark.django_db
class TestTaskFilterService(TestCase):

    def setUp(self):  # ✅ Correct method name for Django TestCase
        now = timezone.now()
        self.task1 = Task.objects.create(title="Buy milk", description="Milk from store", completed=False, updated_at=now)
        self.task2 = Task.objects.create(title="Read book", description="Read a novel", completed=False, updated_at=now)

    def test_filter_by_valid_date(self):
        factory = APIRequestFactory()
        django_request = factory.get('/tasks/?search_date=' + self.task1.updated_at.strftime("%Y-%m-%d"))
        request = Request(django_request)
        queryset = Task.objects.all()
        filtered_queryset, error = TaskFilterService.filter_queryset(request, queryset)
        assert not error
        assert filtered_queryset.count() >= 1

    def test_filter_by_invalid_date_format(self):
        factory = APIRequestFactory()
        django_request = factory.get('/tasks/?search_date=12-12-2024')
        request = Request(django_request)
        queryset = Task.objects.all()
        filtered_queryset, error = TaskFilterService.filter_queryset(request, queryset)
        assert error == "Invalid date format. Please use YYYY-MM-DD."
        assert filtered_queryset.count() == 0

    def test_filter_by_title(self):
        factory = APIRequestFactory()
        django_request = factory.get('/tasks/?search=milk')
        request = Request(django_request)
        queryset = Task.objects.all()
        filtered_queryset, error = TaskFilterService.filter_queryset(request, queryset)
        assert not error
        assert filtered_queryset.first().title == "Buy milk"

    def test_sort_by_date_true(self):
        factory = APIRequestFactory()
        django_request = factory.get('/tasks/?sort_by_date=true')
        request = Request(django_request)
        queryset = Task.objects.all()
        filtered_queryset, error = TaskFilterService.filter_queryset(request, queryset)
        assert not error
        assert list(filtered_queryset) == list(queryset.order_by('-updated_at'))

    def test_sort_by_date_invalid_value(self):
        factory = APIRequestFactory()
        django_request = factory.get('/tasks/?sort_by_date=abc')
        request = Request(django_request)
        queryset = Task.objects.all()
        filtered_queryset, error = TaskFilterService.filter_queryset(request, queryset)
        assert error == "Invalid value for sort_by_date. It must be 'true'."
        assert filtered_queryset.count() == 0

# -------------------------------
# Integration Tests for Task APIs
# -------------------------------
@pytest.mark.django_db
class TestTaskAPI:

    def setup_method(self):
        now = timezone.now()
        self.task1 = Task.objects.create(title="Buy milk", description="Milk", completed=False, updated_at=now)
        self.task2 = Task.objects.create(title="Read book", description="Read", completed=False, updated_at=now)
        self.client = APIClient()
        self.list_url = reverse('task-list')

    def test_create_task_success(self):
        payload = {"title": "Walk dog", "description": "Evening walk", "completed": False}
        response = self.client.post(self.list_url, payload)
        assert response.status_code == 201
        assert response.data["message"] == "Task created successfully."

    def test_create_task_empty_title(self):
        payload = {"title": "   ", "description": "No title", "completed": False}
        response = self.client.post(self.list_url, payload)
        assert response.status_code == 400
        assert "This field may not be blank." in str(response.data)

    def test_list_tasks_success(self):
        response = self.client.get(self.list_url)
        assert response.status_code == 200
        assert len(response.data) >= 2

    def test_search_task_by_title_found(self):
        response = self.client.get(self.list_url, {'search': 'milk'})
        assert response.status_code == 200
        assert "Buy milk" in str(response.data)

    def test_search_task_by_title_not_found(self):
        response = self.client.get(self.list_url, {'search': 'banana'})
        assert response.status_code == 404
        assert "No tasks found" in response.data["message"]

    def test_filter_task_by_valid_date(self):
        response = self.client.get(self.list_url, {'search_date': self.task1.updated_at.strftime("%Y-%m-%d")})
        assert response.status_code == 200
        assert "Buy milk" in str(response.data)

    def test_filter_task_by_invalid_date_format(self):
        response = self.client.get(self.list_url, {'search_date': '12-12-2024'})
        assert response.status_code == 400
        assert "Invalid date format" in response.data["message"]

    def test_update_task_success(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.patch(url, {"completed": True})
        assert response.status_code == 200
        assert response.data["message"] == "Task updated successfully."

    def test_update_task_invalid_id(self):
        url = reverse('task-detail', kwargs={'pk': 'abc'})
        response = self.client.patch(url, {"completed": True})
        assert response.status_code == 400
        assert "Invalid task ID format" in str(response.data)

    def test_delete_task_success(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)
        assert response.status_code == 200
        assert "deleted successfully" in response.data["message"]

    def test_delete_task_not_found(self):
        url = reverse('task-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        assert response.status_code == 404
        assert "Task not found" in str(response.data)


