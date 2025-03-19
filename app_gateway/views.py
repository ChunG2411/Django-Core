from django.contrib.admin.models import LogEntry
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, generics
from rest_framework import permissions

from .preload import *
from .serializer import LogEntrySerializer
from app_account.models import User
from backend.custom.paginator import CustomPagination
from backend.custom.views import PreloadObject


# Create your views here.

app_label = __name__.split('.')[0]


class LogEntryView(ViewSet,
                    generics.ListAPIView,
                    generics.RetrieveAPIView,
                    PreloadObject):
    
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPagination
    preload = LogEntry_preload

    def get_queryset(self): 
        new_queryset = LogEntry.objects.all()
        
        username = self.request.query_params.get('username')

        if username:
            try:
                user = User.objects.get(username=username)
                new_queryset = new_queryset.filter(user=user)
            except:
                new_queryset = []

        return new_queryset
