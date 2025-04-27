from rest_framework import viewsets
from .serializer import TaskSerializer  # Ensure TaskSerializer is imported correctly
from .models import Task
from django.utils import timezone
from rest_framework import filters
from django.db.models import Q

class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        queryset = Task.objects.all()

        # Search by Title
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)  # Filter by title (case-insensitive)

        # Search by Date (created_at date)
        search_date = self.request.query_params.get('search_date')
        if search_date:
            try:
                # Parse the date string from the request
                # Make sure 'search_date' is in the correct format (e.g., "YYYY-MM-DD")
                parsed_date = timezone.datetime.strptime(search_date, "%Y-%m-%d").date()
                queryset = queryset.filter(created_at__date=parsed_date)
            except ValueError:
                pass  # Handle invalid date format gracefully (optional)

        # Sort by Date (descending order - newest first)
        sort_by_date = self.request.query_params.get('sort_by_date')
        if sort_by_date == 'true':
            queryset = queryset.order_by('-created_at')  # Ensure 'created_at' exists in the model

        return queryset
