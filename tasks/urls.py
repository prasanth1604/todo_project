from rest_framework import routers
from tasks import views
from .views import TaskViewSet
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# api versioning
router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
# ]

urlpatterns = router.urls