from import_export import resources
from .models import Article


# Create your models here.

class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article