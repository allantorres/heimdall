from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AgentViewSet  # Add AgentViewSet to imports

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'agents', AgentViewSet, basename='agent')

urlpatterns = [
    path('', include(router.urls)),
]