from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import APIKey, User, VerifyEmail
from .forms import APIKeyForm
from .resources import UserResource
from backend.custom.admin import BaseAdmin, BaseTranslatableAdmin, BaseAdminFunction, BaseImportExportAdmin


# Register your models here.


class APIKeyAdmin(BaseTranslatableAdmin):
    fields = ['id', 'name', 'des', 'expires', 'permissions', 'created_at', 'created_by', 'updated_at', 'updated_by'] + BaseTranslatableAdmin.base_fields
    readonly_fields = ['id'] + BaseTranslatableAdmin.base_readonly_fields
    search_fields = ["translations__name__icontains"]

    list_display = BaseTranslatableAdmin.base_list_display + ["id", "name", "get_expires"] + BaseTranslatableAdmin.base_list_display_custom
    list_display_links = ["id", "name"] + BaseTranslatableAdmin.base_list_display_links
    list_filter = BaseTranslatableAdmin.base_list_filter
    list_per_page = 10

    form = APIKeyForm


class CustomUserAdmin(BaseAdminFunction, UserAdmin, BaseImportExportAdmin):
    list_display = ["username", "email", "email_verified", "phone_verified", "is_active", "is_staff", "is_superuser"]
    list_display_links = ["username", "email"]
    fieldsets = (
        (None,
            {"fields": (
                "username",
                "password",
                "email",
                "email_verified",
                "phone",
                "phone_verified"
            )}
        ),
        (_("Personal info"),
            {"fields": (
                "first_name",
                "last_name",
                "gender",
                "birth",
                "address",
                "avatar_preveiw",
                "avatar",
                "bio",
                "public"
            )}
        ),
        (_("Permissions"),
            {"fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )}
        ),
        (_("Important dates"),
            {"fields": (
                "last_login",
                "date_joined",
                "created_at",
                "updated_at"
            )}
        )
    )
    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "email", "usable_password", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ["avatar_preveiw", "date_joined", "last_login", "created_at", "updated_at"]

    resource_classes = [UserResource]

    def has_import_permission(self, request):
        return False

    @admin.display(description='')
    def avatar_preveiw(self, obj):
        if obj.avatar:
            return mark_safe(f"<a href='{settings.API_URL + obj.avatar.url}' target='_blank'><img src={obj.avatar.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""


class VerifyEmailAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'code', 'created_at', 'created_by', 'updated_at', 'updated_by']
    readonly_fields = ['id', 'created_at', 'created_by', 'updated_at', 'updated_by']
    search_fields = ["name__icontains"]

    list_display = ["id", "user", "code"]
    list_display_links = ["id", "user", "code"]
    list_per_page = 10



admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(VerifyEmail, VerifyEmailAdmin)