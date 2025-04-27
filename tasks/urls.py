from rest_framework import routers
from tasks import views

router = routers.DefaultRouter()
router.register(r"tasks", views.TaskView, "task")

urlpatterns = router.urls
