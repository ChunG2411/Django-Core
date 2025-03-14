from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields
from django_resized import ResizedImageField
from django.contrib.auth.models import Permission
from django.conf import settings

from backend.custom.models import BaseModel, BaseTranslatableModel
from backend.custom.functions import upload_to, create_slug


# Create your models here.

app_label = __name__.split('.')[0]


class APIKey(BaseTranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=1000, verbose_name=_("Tên")),
        des = models.TextField(null=True, blank=True, verbose_name=_("Mô tả")),
    )
    expires = models.DateTimeField(verbose_name=_("Hạn sử dụng"))
    permissions = models.ManyToManyField(Permission, blank=True, related_name="APIKey_permission", verbose_name=_("Quyền truy cập"))
    
    class Meta:
        ordering = ['order', 'created_at']
        db_table = f'tb_{app_label}_apikey'
        verbose_name = _('API Key')
        verbose_name_plural = _('API Key')
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or str(self.id)
    
    def save(self, *args, **kwargs):
        self.slug = create_slug(self.safe_translation_getter('name', language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE))
        super().save(*args, **kwargs)
    
    @admin.display(description=_('Hạn dùng'))
    def get_expires(self):
        return timezone.now() < self.expires
    get_expires.boolean = True
