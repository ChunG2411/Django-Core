from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Image, Document, Link
from .forms import ArticleForm, LinkForm
from .resources import ArticleResource
from backend.custom.admin import BaseAdmin, BaseTranslatableAdmin, BaseTabularInlineAdmin, BaseStackedInlineAdmin, BaseImportExportAdmin


# Register your models here.

app_label = __name__.split('.')[0]


class ImageAdmin(BaseStackedInlineAdmin):
    model = Image
    extra = 0

    fields = ['article', 'thumbnail_preveiw', 'thumbnail', 'file_preveiw', 'file'] + BaseStackedInlineAdmin.base_fields
    readonly_fields = ['thumbnail_preveiw', 'file_preveiw'] + BaseStackedInlineAdmin.base_readonly_fields

    @admin.display(description='')
    def thumbnail_preveiw(self, obj):
        if obj.thumbnail:
            return mark_safe(f"<a href='{settings.API_URL + obj.thumbnail.url}' target='_blank'><img src={obj.thumbnail.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""
    
    @admin.display(description='')
    def file_preveiw(self, obj):
        if obj.file:
            return mark_safe(f"<a href='{settings.API_URL + obj.file.url}' target='_blank'><img src={obj.file.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""
    
    
class DocumentAdmin(BaseTabularInlineAdmin):
    model = Document
    extra = 0

    fields = ['article', 'thumbnail_preveiw', 'thumbnail', 'file'] + BaseTabularInlineAdmin.base_fields
    readonly_fields = ['thumbnail_preveiw'] + BaseTabularInlineAdmin.base_readonly_fields

    @admin.display(description='')
    def thumbnail_preveiw(self, obj):
        if obj.thumbnail:
            return mark_safe(f"<a href='{settings.API_URL + obj.thumbnail.url}' target='_blank'><img src={obj.thumbnail.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""


class LinkAdmin(BaseTabularInlineAdmin):
    model = Link
    extra = 0

    fields = ['name', 'link', 'article', 'thumbnail_preveiw', 'thumbnail'] + BaseTabularInlineAdmin.base_fields
    readonly_fields = ['thumbnail_preveiw'] + BaseTabularInlineAdmin.base_readonly_fields

    form = LinkForm

    @admin.display(description='')
    def thumbnail_preveiw(self, obj):
        if obj.thumbnail:
            return mark_safe(f"<a href='{settings.API_URL + obj.thumbnail.url}' target='_blank'><img src={obj.thumbnail.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""
        

class ArticleAdmin(
                    BaseTranslatableAdmin,
                    SummernoteModelAdmin,
                    BaseImportExportAdmin
                    ):
    fields = ['name', 'abstract', 'content', 'thumbnail_preveiw', 'thumbnail', 'view', 'like', 'approve'] + BaseTranslatableAdmin.base_fields
    readonly_fields = ['thumbnail_preveiw'] + BaseTranslatableAdmin.base_readonly_fields
    search_fields = ["translations__name__icontains"]

    list_display = BaseTranslatableAdmin.base_list_display + ["name", "thumbnail_tag", "view", "like", "approve"] + BaseTranslatableAdmin.base_list_display_custom
    list_display_links = ["name"] + BaseTranslatableAdmin.base_list_display_links
    list_filter = BaseTranslatableAdmin.base_list_filter
    list_per_page = 10

    summernote_fields = ["content"]
    form = ArticleForm
    resource_classes = [ArticleResource]

    inlines = [
        ImageAdmin,
        DocumentAdmin,
        LinkAdmin
    ]

    def has_import_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj = ...):
        if request.user.is_superuser or request.user.has_perm(f'{app_label}.can_approve_article'):
            return super().get_readonly_fields(request, obj)
        return super().get_readonly_fields(request, obj) + ['approve']

    @admin.display(description='')
    def thumbnail_preveiw(self, obj):
        if obj.thumbnail:
            return mark_safe(f"<a href='{settings.API_URL + obj.thumbnail.url}' target='_blank'><img src={obj.thumbnail.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""
    
    @admin.display(description='Ảnh thu nhỏ')
    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return mark_safe(f"<a href='{settings.API_URL + obj.thumbnail.url}' target='_blank'><img src={obj.thumbnail.url} style='width:100px;height:100px;object-fit:contain'/></a>")
        else:
            return ""


admin.site.register(Article, ArticleAdmin)