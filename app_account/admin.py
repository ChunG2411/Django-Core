from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin

from .models import APIKey
from .forms import APIKeyForm
from backend.custom.admin import BaseAdmin, BaseTranslatableAdmin, BaseTabularInlineAdmin, BaseStackedInlineAdmin


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


admin.site.register(APIKey, APIKeyAdmin)