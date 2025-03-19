from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LogEntryView


routers = DefaultRouter()
routers.register('log', LogEntryView, basename='log')


urlpatterns = [
    path('', include(routers.urls)),

    path("app_article/", include('app_article.urls')),
    path("app_account/", include('app_account.urls')),

]