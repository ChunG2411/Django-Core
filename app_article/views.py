from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions

from .models import (
                        Article,
                        Image,
                        Document,
                        Link
                    )
from .seralizers import (
                            ArticleSerializer, ArticleOverviewSerializer,
                            ImageSerializer, ImageOverviewSerializer,
                            DocumentSerializer, DocumentOverviewSerializer,
                            LinkSerializer, LinkOverviewSerializer
                        )
from .preload import *
from backend.custom.paginator import CustomPagination
from backend.custom.views import PreloadObject, HandleDestroy, HandleHideShowObject
from backend.custom.permissions import CustomModelPermissions, SpecialModelPermissions


# Create your views here.

app_label = __name__.split('.')[0]


class ArticleView(ModelViewSet,
                  HandleDestroy,
                  HandleHideShowObject,
                  PreloadObject):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [CustomModelPermissions]
    pagination_class = CustomPagination
    preload = Article_preload

    def get_queryset(self): 
        new_queryset = Article.objects.all()
        
        name = self.request.query_params.get('name')
        approve = self.request.query_params.get('approve')

        if name:
            new_queryset = new_queryset.filter(translations__name__icontains=name.lower()).distinct()
        if approve == '1':
            new_queryset = Article.objects.filter(approve=True)
        elif approve == '0':
            new_queryset = Article.objects.filter(approve=False)
        elif approve == 'all':
            new_queryset = Article.objects.all()

        return new_queryset

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return ArticleOverviewSerializer
        else:
            return ArticleSerializer
        
    def get_permissions(self):
        if self.action in ['handle_approve']:
            return [SpecialModelPermissions(perm='can_approve_article')]
        else:
            return [CustomModelPermissions()]
    
    @action(methods=['get'], detail=True, url_path='approve')
    def handle_approve(self, request, pk):
        action = self.request.query_params.get('action')
        obj = self.get_object()
        if action == '1':
            obj.approve = True
        else:
            obj.approve = False
        obj.save()
        return Response(self.get_serializer_class()(obj).data, status=200)
