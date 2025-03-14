from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone


class HandleHideShowObject():
    @action(methods=['get'], detail=True, url_path='deactive')
    def hide_object(self, request, pk):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response(self.get_serializer_class()(obj).data, status=200)
    
    @action(methods=['get'], detail=True, url_path='active')
    def show_object(self, request, pk):
        obj = self.get_object()
        obj.is_active = True
        obj.save()
        return Response(self.get_serializer_class()(obj).data, status=200)
    

class PreloadObject():
    @action(methods=['get'], detail=False, url_path='preload')
    def get_preload(self, request):
        return Response(self.preload, status=200)


class HandleDestroy():
    def delete(self, request, pk):
        obj = self.get_object()
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_by = request.user
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
        return Response("", status=204)