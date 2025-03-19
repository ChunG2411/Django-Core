from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
                        APIKeyView,
                        UserView,
                        GroupView
                    )


# Create your urls here.

routers = DefaultRouter()
routers.register('api-key', APIKeyView, basename='api_key')
routers.register('user', UserView, basename='user')
routers.register('group', GroupView, basename='group')


urlpatterns = [
    path('', include(routers.urls)),
]

