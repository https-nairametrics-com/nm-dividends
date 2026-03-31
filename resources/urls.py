"""
URL configuration for the resources app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, MediaFileViewSet

# Create router for viewsets
router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'media', MediaFileViewSet, basename='mediafile')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]

# Additional URL patterns for custom actions
# The categories action is available at: GET /api/v1/resources/categories/
# This is handled by the @action decorator in ResourceViewSet
