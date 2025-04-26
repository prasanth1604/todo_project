from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list_page, name="task_list_page"),  # Renders HTML
    path("api/", views.task_list_create, name="task_list_create"),  # API
    path("api/<int:id>/", views.task_delete_patch, name="task_delete_patch"),  # API
]
