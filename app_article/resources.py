from import_export import resources, fields
from django.conf import settings

from .models import Article


# Create your models here.

class ArticleResource(resources.ModelResource):
    name = fields.Field()
    abstract = fields.Field()
    content = fields.Field()

    class Meta:
        model = Article
        fields = ('id', 'name', 'abstract', 'content', 'thumbnail', 'view', 'like', 'approve', 'is_active')

    def import_instance(self, instance, row, **kwargs):
        super().import_instance(instance, row, **kwargs)
        instance.set_current_language(settings.PARLER_DEFAULT_LANGUAGE_CODE)
        instance.name = row['name']
        instance.save()
    
    def dehydrate_name(self, model_instance):
        try:
            name = model_instance.get_translation(language_code=model_instance.language_code).name
        except:
            name = ""
        return name

    def dehydrate_abstract(self, model_instance):
        try:
            abstract = model_instance.get_translation(language_code=model_instance.language_code).abstract
        except:
            abstract = ""
        return abstract

    def dehydrate_content(self, model_instance):
        try:
            content = model_instance.get_translation(language_code=model_instance.language_code).content
        except:
            content = ""
        return content