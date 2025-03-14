from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
                     ArticleView   
                    )


# Create your urls here.

routers = DefaultRouter()
routers.register('article', ArticleView, basename='app_article_article')


urlpatterns = [
    path('', include(routers.urls)),
]

