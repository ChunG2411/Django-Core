from django.urls import path, include


urlpatterns = [
    path("app_article/", include('app_article.urls')),
    path("app_account/", include('app_account.urls')),

]