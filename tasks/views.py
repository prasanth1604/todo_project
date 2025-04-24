from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import TaskSerialize
from .models import Task
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data
        })


class TaskView(viewsets.ViewSet):
    serializer_class = TaskSerialize
    queryset = Task.objects.all()  # Initialize queryset at the class level
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        tasks = self.queryset  # Use the class-level queryset

        # Sorting
        sort_by_date = request.query_params.get('sort_by_date')
        if sort_by_date:
            tasks = tasks.order_by('created_at')  # Sort by creation date

        # Date Searching
        search_date_str = request.query_params.get('search_date')
        if search_date_str:
            try:
                search_date = timezone.datetime.strptime(search_date_str, '%Y-%m-%d').date()
                tasks = tasks.filter(created_at__date=search_date)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Title Searching
        search_title = request.query_params.get('search')
        if search_title:
            tasks = tasks.filter(title__icontains=search_title)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(tasks, request)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        task = get_object_or_404(self.queryset, pk=pk) # Use class queryset
        serializer = self.serializer_class(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        task = get_object_or_404(self.queryset, pk=pk) # Use class queryset
        serializer = self.serializer_class(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = get_object_or_404(self.queryset, pk=pk) # Use class queryset
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        completed_tasks = self.queryset.filter(completed=True)
        serializer = self.serializer_class(completed_tasks, many=True)
        return Response(serializer.data)
