from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializer import TaskSerializer
from .filters import TaskFilter

class TaskViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update`, `partial_update`, and `destroy`
    actions for Task. Supports filtering by date/title and sorting by date.
    """
    queryset         = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer

    # Use a FilterSet to keep filtering logic out of the view itself
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
