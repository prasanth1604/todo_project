import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    """
    Defines the query-params we support:
      - search:   case-insensitive title contains
      - search_date: exact match on date
      - sort_by_date: special ordering
    """
    search       = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title contains')
    search_date  = django_filters.DateFilter(field_name='date', lookup_expr='exact', label="Date")
    sort_by_date = django_filters.BooleanFilter(method='filter_sort', label = 'Sort by date')

    class Meta:
        model  = Task
        fields = ['search', 'search_date', 'sort_by_date']

    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by('date')
        return queryset
