from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer



class BaseRepSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
    
    def to_representation(self, instance):
        fields = self.context.get('request').GET.get('fields', 'all')

        data = super().to_representation(instance)
        
        if not fields == 'all':
            fields_list = [i.strip() for i in fields.split(',')]
            for i in list(data.keys()):
                if i not in fields_list:
                    del data[i]

        return data


class BaseRepTranslatableSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
    
    def to_representation(self, instance):
        language = self.context.get('request').GET.get('language', 'vi')
        fields = self.context.get('request').GET.get('fields', 'all')

        data = super().to_representation(instance)
        if not language == 'all':
            data["translations"] = { language: data["translations"][language] } if language in data["translations"] else { language: None }
        
        if not fields == 'all':
            fields_list = [i.strip() for i in fields.split(',')] + ["translations"]
            for i in list(data["translations"].keys()):
                for j in list(data["translations"][i].keys()):
                    if j not in fields_list:
                        del data["translations"][i][j]
            for i in list(data.keys()):
                if i not in fields_list:
                    del data[i]

        return data


class BaseSerializer(BaseRepSerializer):
    base_fields = [
                    "id", "order", "slug",
                   "is_active",
                   "created_at", "created_by",
                   "updated_at", "updated_by"
                ]
    base_overview_fields = ["id", "order", "slug", "is_active"]

    class Meta:
        abstract = True
    

class BaseTranslatableSerializer(BaseRepTranslatableSerializer, TranslatableModelSerializer):
    base_fields = [
                    "id", "order", "slug",
                   "is_active",
                   "created_at", "created_by",
                   "updated_at", "updated_by"
                ]
    base_overview_fields = ["id", "order", "slug", "is_active"]

    class Meta:
        abstract = True
