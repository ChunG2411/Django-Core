from rest_framework import serializers
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

from backend.custom.serializers import BaseSerializer, BaseTranslatableSerializer, BaseRepSerializer


# Create your serializers here.

app_label = __name__.split('.')[0]


class LogEntrySerializer(BaseRepSerializer):
    user = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    action_flag = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = ["id", "user", "object_id", "content_type", "action_flag", "action_time"]
    
    def get_user(self, obj):
        return {
            "id": str(obj.user.id),
            "username": obj.user.username
        } if obj.user else None

    def get_content_type(self, obj):
        return {
            "id": str(obj.content_type.id),
            "app_label": obj.content_type.app_label,
            "model": obj.content_type.model
        } if obj.content_type else None

    def get_action_flag(self, obj):
        if obj.action_flag == 1:
            return "Addition"
        elif obj.action_flag == 2:
            return "Change"
        else:
            return "Deletion"