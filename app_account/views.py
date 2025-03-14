from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions

from .models import (
                        APIKey
                    )
from .seralizers import (
                            APIKeySerializer, APIKeyOverviewSerializer,
                        )
from .preload import *
from backend.custom.paginator import CustomPagination
from backend.custom.views import PreloadObject, HandleDestroy, HandleHideShowObject
from backend.custom.permissions import CustomModelPermissions, SpecialModelPermissions


# Create your views here.

app_label = __name__.split('.')[0]


class APIKeyView(ModelViewSet,
                  HandleDestroy,
                  HandleHideShowObject,
                  PreloadObject):
    
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    permission_classes = [CustomModelPermissions]
    pagination_class = CustomPagination
    preload = APIKey_preload

    def get_queryset(self): 
        new_queryset = APIKey.objects.all()
        
        name = self.request.query_params.get('name')

        if name:
            new_queryset = new_queryset.filter(translations__name__icontains=name.lower()).distinct()

        return new_queryset

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return APIKeyOverviewSerializer
        else:
            return APIKeySerializer

