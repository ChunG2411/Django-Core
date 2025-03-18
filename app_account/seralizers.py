from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import (
                        APIKey,
                        User
                    )
from backend.custom.serializers import BaseSerializer, BaseTranslatableSerializer


# Create your serializers here.

app_label = __name__.split('.')[0]


# APIKey

class APIKeySerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=APIKey)

    class Meta:
        model = APIKey
        ref_name = app_label
        fields = [
            'translations',
            'expires',
            'permissions'
        ] + BaseTranslatableSerializer.base_fields


class APIKeyOverviewSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=APIKey)

    class Meta:
        model = APIKey
        ref_name = app_label
        fields = [
            'translations',
            'expires'
        ] + BaseTranslatableSerializer.base_overview_fields
    