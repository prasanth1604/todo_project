from rest_framework import viewsets, filters
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    filterset_fields = ['completed']

    def get_queryset(self):
        queryset = Task.objects.all()
        # sort_by_date=true
        sort = self.request.query_params.get('sort_by_date')
        if sort == 'true':
            queryset = queryset.order_by('-id')

        # search_date=YYYY-MM-DD
        search_date = self.request.query_params.get('search_date')
        if search_date:
            date_obj = parse_date(search_date)
            queryset = queryset.filter(created_at__date=date_obj)

        return queryset

