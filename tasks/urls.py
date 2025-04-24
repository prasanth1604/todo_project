from django.urls import path
from rest_framework import routers
from tasks import views

# api versioning
router = routers.DefaultRouter()
router.register(r"tasks", views.TaskView, "task")

urlpatterns = router.urls
urlpatterns += [
    path('tasks/completed/', views.TaskView.as_view({'get': 'completed'}), name='task-completed'),
]