from django.contrib import admin
from django.utils import timezone
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from import_export.admin import ImportExportModelAdmin
from django.utils.timezone import datetime


class BaseAdmin(admin.ModelAdmin):
    base_readonly_fields = ["created_by", "created_at", "updated_by", "updated_at", "is_deleted", "deleted_by", "deleted_at", "slug"]
    base_fields = ["order", "is_active"]

    base_list_display = ["order"]
    base_list_display_custom = ["is_active"]
    base_list_display_links = ["order"]
    base_list_filter = ["is_active"]

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_by = request.user
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.is_deleted:
                obj.delete()
            else:
                obj.is_deleted = True
                obj.deleted_by = request.user
                obj.deleted_at = timezone.now()
                obj.save()


class BaseTranslatableAdmin(TranslatableAdmin):
    base_readonly_fields = ["created_by", "created_at", "updated_by", "updated_at", "is_deleted", "deleted_by", "deleted_at", "slug"]
    base_fields = ["order", "is_active"]

    base_list_display = ["order"]
    base_list_display_custom = ["is_active"]
    base_list_display_links = ["order"]
    base_list_filter = ["is_active"]

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_by = request.user
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.is_deleted:
                obj.delete()
            else:
                obj.is_deleted = True
                obj.deleted_by = request.user
                obj.deleted_at = timezone.now()
                obj.save()


class BaseStackedInlineAdmin(admin.StackedInline):
    base_readonly_fields = ["created_by", "created_at", "updated_by", "updated_at", "is_deleted", "deleted_by", "deleted_at", "slug"]
    base_fields = ["is_active"]

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_by = request.user
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.is_deleted:
                obj.delete()
            else:
                obj.is_deleted = True
                obj.deleted_by = request.user
                obj.deleted_at = timezone.now()
                obj.save()


class BaseTabularInlineAdmin(admin.TabularInline, TranslatableTabularInline):
    base_readonly_fields = ["created_by", "created_at", "updated_by", "updated_at", "is_deleted", "deleted_by", "deleted_at", "slug"]
    base_fields = ["is_active"]
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        if not obj.is_deleted:
            obj.is_deleted = True
            obj.deleted_by = request.user
            obj.deleted_at = timezone.now()
            obj.save()
        else:
            obj.delete()
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.is_deleted:
                obj.delete()
            else:
                obj.is_deleted = True
                obj.deleted_by = request.user
                obj.deleted_at = timezone.now()
                obj.save()


class BaseImportExportAdmin(ImportExportModelAdmin):
    def get_export_filename(self, request, queryset, file_format):
        return f"{self.model.__name__}-{datetime.now().strftime('%Y-%m-%d')}-{request.LANGUAGE_CODE}.{file_format.get_extension()}"