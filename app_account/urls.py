from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
                        APIKeyView
                    )


# Create your urls here.

routers = DefaultRouter()
routers.register('api-key', APIKeyView, basename='api_key')


urlpatterns = [
    path('', include(routers.urls)),
]

