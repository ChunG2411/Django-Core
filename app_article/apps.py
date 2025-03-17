from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppArticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_article'
    verbose_name = _('Bài viết')
