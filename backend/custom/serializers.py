from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer


class BaseSerializer(serializers.ModelSerializer):
    base_fields = [
                    "id", "order", "slug",
                   "is_active",
                   "created_at", "created_by",
                   "updated_at", "updated_by"
                ]
    base_overview_fields = ["id", "order", "slug", "is_active"]

    class Meta:
        abstract = True


class BaseTranslatableSerializer(BaseSerializer, TranslatableModelSerializer):
    class Meta:
        abstract = True
    
    def to_representation(self, instance):
        language = self.context.get('request').GET.get('language', 'vi')
        data = super().to_representation(instance)
        if not language == 'all':
            data["translations"] = { language: data["translations"][language] } if language in data["translations"] else { language: None }
        return data