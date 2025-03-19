from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework import permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.models import AccessToken, RefreshToken
from dotenv import load_dotenv
import os, json
from django.utils import timezone

from .models import (
                        APIKey,
                        User,
                        VerifyEmail
                    )
from .seralizers import (
                            APIKeySerializer, APIKeyOverviewSerializer,
                            UserSerializer, UserOverviewSerializer,
                            GroupSerializer, GroupOverviewSerializer
                        )
from .preload import *
from backend.custom.paginator import CustomPagination
from backend.custom.views import PreloadObject, HandleDestroy, HandleHideShowObject
from backend.custom.permissions import CustomModelPermissions, SpecialModelPermissions, IsOwnerPermission
from backend.custom.functions import check_validate_password, get_random_password, get_random_verify
from backend.custom.task import send_email_task

# Create your views here.

app_label = __name__.split('.')[0]
load_dotenv()


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(OAuthLibMixin, View):
    # @staticmethod
    # def save_log_authen(request, user):
    #     ip_address = get_ip_address(request)
    #     platform = request.META.get('HTTP_SEC_CH_UA_PLATFORM')
    #     info_machine = request.META.get('HTTP_USER_AGENT')
    #     LogAuthen.objects.create(user=user, ip_address=ip_address, platform=platform, info_machine=info_machine,
    #                              action = 'Login')

    def post(self, request, *args, **kwargs):
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')
        user = None
        try:
            if '@' in username_email:
                username = User.objects.get(email=username_email).username
                user = authenticate(username=username, password=password)
            else:
                user = authenticate(username=username_email, password=password)
            if not user:
                return HttpResponse("Tên đăng nhập hoặc mật khẩu không đúng", status=400)
        except:
            return HttpResponse("Tên đăng nhập hoặc Email không tồn tại", status=400)
        
        post = request.POST.copy()
        post['username'] = user.username
        post['client_id'] = os.getenv('CLIENT_ID')
        post['client_secret'] = os.getenv('CLIENT_SECRET')
        post['grant_type'] = 'password'
        request.POST = post

        _, _, body, status = self.create_token_response(request)
        body = json.loads(body)
        if status == 200:
            # self.save_log_authen(request, user)
            user.last_login = timezone.now()
            user.save()
        return JsonResponse(data=body, status=status)


@permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    # @staticmethod
    # def save_log_authen(request, action):
    #     ip_address = get_ip_address(request)
    #     platform = request.META.get('HTTP_SEC_CH_UA_PLATFORM')
    #     info_machine = request.META.get('HTTP_USER_AGENT')
    #     LogAuthen.objects.create(user=request.user, ip_address=ip_address, platform=platform, info_machine=info_machine,
    #                              action = action)
        
    def post(self, request):
        all = request.data.get('all')
        try:
            if all:
                access_token = AccessToken.objects.filter(user=request.user)
                refresh_token = RefreshToken.objects.filter(user=request.user)
                access_token.delete()
                refresh_token.delete()
                # self.save_log_authen(request, 'Logout all')
                return Response("Đã đăng xuất khỏi tất cả thiết bị", status=200)
            else:
                access_token = AccessToken.objects.get(token=request.auth)
                refresh_token = RefreshToken.objects.get(access_token=access_token)
                access_token.delete()
                refresh_token.delete()
                # self.save_log_authen(request, 'Logout')
                return Response("Đã đăng xuất", status=200)
        except:
            return Response("Có lỗi xảy ra trong quá trình thực hiện", status=400)
        

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
    
    @action(methods=['post'], detail=True, url_path='add-permission')
    def add_permission(self, request, pk):
        per_request = request.data.get('permission')
        per_codename = request.data.get('permission_codename')
        all = request.data.get('all')

        key = self.get_object()
        if all:
            for i in Permission.objects.all():
                key.permissions.add(i)
        else:
            if per_request:
                per_list = per_request.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.get(id=i.strip())
                        key.permissions.add(permission)
                    except:
                        pass
            elif per_codename:
                per_list = per_codename.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.filter(codename=i.strip())
                        key.permissions.add(permission[0])
                    except:
                        pass
        serializer = self.get_serializer_class()(key, context = {'request': request})
        return Response(serializer.data, status=200)
    
    @action(methods=['post'], detail=True, url_path='remove-permission')
    def remove_permission(self, request, pk):
        per_request = request.data.get('permission')
        per_codename = request.data.get('permission_codename')
        all = request.data.get('all')

        key = self.get_object()
        if all:
            key.permissions.clear()
        else:
            if per_request:
                per_list = per_request.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.get(id=i.strip())
                        key.permissions.remove(permission)
                    except:
                        pass
            elif per_codename:
                per_list = per_codename.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.filter(codename=i.strip())
                        key.permissions.remove(permission[0])
                    except:
                        pass
        serializer = self.get_serializer_class()(key, context = {'request': request})
        return Response(serializer.data, status=200)


class UserView(ModelViewSet,
               HandleDestroy,
               HandleHideShowObject,
               PreloadObject):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [CustomModelPermissions]
    preload = User_preload

    def get_serializer_class(self):
        if self.action in ["retrieve"] and self.kwargs.get('pk') != str(self.request.user.id):
            return UserOverviewSerializer
        elif self.action in ['list']:
            return UserOverviewSerializer
        else:
            return UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'list']:
            return [permissions.AllowAny()]
        elif self.action in ['partial_update']:
            return [IsOwnerPermission()]
        elif self.action in ['get_current_user', 'change_password', 'send_verify_email', 'verify', 'restore_password']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['set_password']:
            return [permissions.IsAdminUser()]
        else:
            return [CustomModelPermissions()]
        
    def get_queryset(self):
        new_queryset = User.objects.all()

        name = self.request.query_params.get('name')
        if name:
            new_queryset = new_queryset.filter(Q(first_name__icontains=name.lower()) | Q(last_name__icontains=name.lower()))
        
        username = self.request.query_params.get('username')
        if username:
            new_queryset = new_queryset.filter(username__icontains=username.lower())
        
        email = self.request.query_params.get('email')
        if email:
            new_queryset = new_queryset.filter(email__icontains=email.lower())
        
        phone = self.request.query_params.get('phone')
        if phone:
            new_queryset = new_queryset.filter(phone__icontains=phone.lower())

        group_id = self.request.query_params.get('groups')
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                new_queryset = new_queryset.filter(groups=group)
            except:
                new_queryset = []

        return new_queryset
    
    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        serializer = self.get_serializer_class()(request.user, context={"request": request})
        return Response(serializer.data, status=200)
    
    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        new_pass = request.data.get('new_pass')
        old_pass = request.data.get('old_pass')

        user = authenticate(username=request.user.username, password=old_pass)
        if user:
            status, msg = check_validate_password(new_pass)
            if not status:
                return Response(msg, status=400)
            if new_pass == old_pass:
                return Response("Mật khẩu mới phải khác mật khẩu cũ", status=400)
            user.set_password(new_pass)
            user.save()
            return Response("Đổi mật khẩu thành công", status=200)
        else:
            return Response("Mật khẩu không chính xác", status=400)
    
    @action(methods=['get'], detail=False, url_path='restore-pass')
    def restore_password(self, request):
        new_pass = get_random_password()
        request.user.set_password(new_pass)
        request.user.save()
        send_email_task.delay(request.user.email, new_pass)
        return Response("Mật khẩu mới đã được gửi đến email của bạn", status=200)
    
    @action(methods=['post'], detail=True, url_path='set-pass')
    def set_password(self, request, pk):
        user = self.get_object()
        password = request.data.get('password')
        status, msg = check_validate_password(password)
        if not status:
            return Response(msg, status=400)
        user.set_password(password)
        user.save()
        return Response("Đã thiết lập mật khẩu mới", status=200)
    
    @action(methods=['get'], detail=False, url_path='send-verify-email')
    def send_verify_email(self, request):
        code_char = get_random_verify()
        try:
            verify = VerifyEmail.objects.get(user=request.user)
            verify.code = code_char
            verify.save()
        except:
            VerifyEmail.objects.create(user=request.user, code=code_char)
        send_email_task.delay(request.user.email, code_char)
        return Response("Đã gửi mã xác thức đến email của bạn", status=200)
    
    @action(methods=['post'], detail=False, url_path='verify-email')
    def verify(self, request):
        code = request.data.get('code')
        verify = VerifyEmail.objects.get(user=request.user)
        if code == verify.code:
            request.user.email_verified = True
            request.user.save()
            return Response("Đã xác thực email", status=200)
        else:
            return Response("Mã xác thực không chính xác", status=400)


class GroupView(ModelViewSet,
                HandleDestroy,
                PreloadObject):
    
    queryset = Group.objects.all()
    pagination_class = CustomPagination
    permission_classes = [CustomModelPermissions]
    preload = Group_preload

    def get_queryset(self):
        new_queryset = Group.objects.all()

        name = self.request.query_params.get('name')
        if name:
            new_queryset = new_queryset.filter(name__icontains=name.lower())

        return new_queryset
    
    def get_serializer_class(self):
        if self.action in ["create", "list"]:
            return GroupOverviewSerializer
        else:
            return GroupSerializer
    
    @action(methods=['post'], detail=True, url_path='add-permission')
    def add_permission(self, request, pk):
        per_request = request.data.get('permission')
        per_codename = request.data.get('permission_codename')
        all = request.data.get('all')

        group = self.get_object()
        if all:
            for i in Permission.objects.all():
                group.permissions.add(i)
        else:
            if per_request:
                per_list = per_request.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.get(id=i.strip())
                        group.permissions.add(permission)
                    except:
                        pass
            elif per_codename:
                per_list = per_codename.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.filter(codename=i.strip())
                        group.permissions.add(permission[0])
                    except:
                        pass
        serializer = self.get_serializer_class()(group, context = {'request': request})
        return Response(serializer.data, status=200)
    
    @action(methods=['post'], detail=True, url_path='remove-permission')
    def remove_permission(self, request, pk):
        per_request = request.data.get('permission')
        per_codename = request.data.get('permission_codename')
        all = request.data.get('all')

        group = self.get_object()
        if all:
            group.permissions.clear()
        else:
            if per_request:
                per_list = per_request.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.get(id=i.strip())
                        group.permissions.remove(permission)
                    except:
                        pass
            elif per_codename:
                per_list = per_codename.split(',')
                for i in per_list:
                    try:
                        permission = Permission.objects.filter(codename=i.strip())
                        group.permissions.remove(permission[0])
                    except:
                        pass
        serializer = self.get_serializer_class()(group, context = {'request': request})
        return Response(serializer.data, status=200)
    
    @action(methods=['post'], detail=True, url_path='add-user')
    def add_user(self, request, pk):
        user_id = request.data.get('user')
        user = User.objects.get(id=user_id)
        group = self.get_object()
        user.groups = group
        user.save()
        serializer = self.get_serializer_class()(group, context = {'request': request})
        return Response(serializer.data, status=200)
    
    @action(methods=['post'], detail=True, url_path='remove-user')
    def remove_user(self, request, pk):
        user_id = request.data.get('user')
        user = User.objects.get(id=user_id)
        group = self.get_object()
        user.groups = None
        user.save()
        serializer = self.get_serializer_class()(group, context = {'request': request})
        return Response(serializer.data, status=200)
    
