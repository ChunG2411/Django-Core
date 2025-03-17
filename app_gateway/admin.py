from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    search_fields = ["user"]
    list_display = ["user", "content_type", "object_link", "action_flag"]
    list_display_links = ["user", "content_type"]
    list_per_page = 10

    def has_add_permission(self, request, obj=None):
        return False
    
    @admin.display(description=_('Đối tượng'))
    def object_link(self, obj):
        return mark_safe(f"<a href='/admin/{obj.content_type.app_label}/{obj.content_type.model}/{obj.object_id}/change/' target='_blank'>{obj.object_id}</a>")


admin.site.register(LogEntry, LogEntryAdmin)