from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json
from django.utils.dateparse import parse_date

@csrf_exempt
def task_list_create(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        
        # Search by title
        search_query = request.GET.get('search')
        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        # Filter by date
        date_query = request.GET.get('date')
        if date_query:
            parsed_date = parse_date(date_query)
            if parsed_date:
                tasks = tasks.filter(creation_date__date=parsed_date)

        # Sort by creation_date
        sort_order = request.GET.get('sort')
        if sort_order == 'asc':
            tasks = tasks.order_by('creation_date')
        elif sort_order == 'desc':
            tasks = tasks.order_by('-creation_date')

        tasks_list = list(tasks.values())
        return JsonResponse(tasks_list, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)
        task = Task.objects.create(
            title=data.get("title", ""),
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )
        return JsonResponse({"id": task.id, "message": "Task created successfully."}, status=201)

@csrf_exempt
def task_delete_patch(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"message": "Task deleted successfully."})

    if request.method == "PATCH":
        data = json.loads(request.body)
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.completed = data.get("completed", task.completed)
        task.save()
        return JsonResponse({"message": "Task updated successfully."})
