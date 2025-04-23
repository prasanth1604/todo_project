from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .serializer import TaskSerialize
from .models import Task
from rest_framework.decorators import action

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerialize

    def get_queryset(self):
        queryset = Task.objects.all()

        # Sorting by date
        if self.request.query_params.get('sort_by_date') == 'true':
            queryset = queryset.order_by('-created_at')  # Sorting by creation date in descending order

        # Search by title
        search_title = self.request.query_params.get('search')
        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        # Search by date
        search_date = self.request.query_params.get('search_date')
        if search_date:
            date = parse_date(search_date)
            if date:
                queryset = queryset.filter(created_at__date=date)

        return queryset

    @action(detail=True, methods=['patch'])
    def update_task(self, request, pk=None):
        task = self.get_object()
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=204)
