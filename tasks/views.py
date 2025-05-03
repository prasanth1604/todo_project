from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializer import TaskSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q

class TaskListCreateView(APIView):
    def get(self, request):
        tasks = Task.objects.all()

        # Search by title
        search_query = request.GET.get('search')
        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        # Search by date
        search_date = request.GET.get('search_date')
        if search_date:
            tasks = tasks.filter(date=search_date)

        # Sort by date
        sort_by_date = request.GET.get('sort_by_date')
        if sort_by_date == 'true':
            tasks = tasks.order_by('date')

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateDeleteView(APIView):
    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
