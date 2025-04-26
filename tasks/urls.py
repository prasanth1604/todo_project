from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list_create, name="task_list_create"),  # GET + POST
    path("<int:id>/", views.task_delete_patch, name="task_delete_patch"),  # DELETE + PATCH
]
