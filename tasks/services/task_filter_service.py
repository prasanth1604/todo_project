from datetime import datetime

class TaskFilterService:
    """Service class for filtering Task queryset based on request parameters."""

    @staticmethod
    def filter_queryset(request, queryset):
        search_date = request.query_params.get('search_date')
        sort_by_date = request.query_params.get('sort_by_date')
        search_title = request.query_params.get('search')
        error_message = None

        if search_date:
            try:
                datetime.strptime(search_date, "%Y-%m-%d")
                queryset = queryset.filter(updated_at__date=search_date)
            except ValueError:
                error_message = "Invalid date format. Please use YYYY-MM-DD."
                return queryset.none(), error_message

        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        if sort_by_date:
            if sort_by_date.lower() == 'true':
                queryset = queryset.order_by('-updated_at')
            else:
                error_message = "Invalid value for sort_by_date. It must be 'true'."
                return queryset.none(), error_message

        return queryset, error_message
