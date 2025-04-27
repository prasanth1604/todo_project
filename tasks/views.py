from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from tasks.services.task_filter_service import TaskFilterService
from .serializers import TaskSerializer
from .models import Task
from datetime import datetime

class TaskViewSet(viewsets.ModelViewSet): 
    """ViewSet for managing Tasks with search, sort, and CRUD operations"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['updated_at']


    def get_queryset(self):
        """Override to allow filtering by search_date, title and sorting by date"""
        queryset = super().get_queryset()
        queryset, self.error_message = TaskFilterService.filter_queryset(self.request, queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        """Handle GET requests for list of tasks with optional filters"""
        queryset = self.filter_queryset(self.get_queryset())

        if self.error_message:
            return Response({"message": self.error_message}, status=status.HTTP_400_BAD_REQUEST)

        if not queryset.exists():
            search_date = request.query_params.get('search_date')
            search_title = request.query_params.get('search')

            if search_date:
                return Response({"message": f"No tasks found for date {search_date}"},status=status.HTTP_404_NOT_FOUND)
            elif search_title:
                return Response({"message": f"No tasks found for title '{search_title}'"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "No tasks found."},status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Handle POST requests to create a new task"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Task created successfully.","task": serializer.data}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """Handle DEL requests"""
        try:
            task = self.get_object()
            task_title = task.title
            self.perform_destroy(task)
            return Response({"message": f"Task '{task_title}' has been deleted successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Task not found or already deleted."},status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests"""
        task_id = kwargs.get('pk') 
        if not task_id.isdigit():  
            raise ValidationError({"error": "Invalid task ID format. ID must be numeric."}, code=status.HTTP_400_BAD_REQUEST)
        
        if not request.data:
         raise ValidationError({"error": "Empty update not allowed."}, code=status.HTTP_400_BAD_REQUEST)
        
        kwargs['partial'] = True
        try:
            instance = self.get_object()
        except:
            raise NotFound(detail="Task not found.")
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({"message": "Task updated successfully.","task": serializer.data})
