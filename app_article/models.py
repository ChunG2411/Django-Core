from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields
from django_resized import ResizedImageField
from django.conf import settings

from backend.custom.models import BaseModel, BaseTranslatableModel
from backend.custom.functions import upload_to, validate_document_extension, create_slug


# Create your models here.

app_label = __name__.split('.')[0]


class Article(BaseTranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=1000, verbose_name=_("Tên")),
        abstract = models.TextField(null=True, blank=True, verbose_name=_("Tóm tắt")),
        content = models.TextField(null=True, blank=True, verbose_name=_("Nội dung"))
    )
    thumbnail = ResizedImageField( upload_to=upload_to, max_length=1000, null=True, blank=True, verbose_name=_("Ảnh thu nhỏ"))
    view = models.IntegerField(default=0, verbose_name=_("Lượt xem"))
    like = models.IntegerField(default=0, verbose_name=_("Lượt thích"))
    approve = models.BooleanField(default=False, verbose_name=_("Phê duyệt"))

    class Meta:
        ordering = ['order', 'created_at']
        db_table = f'tb_{app_label}_article'
        verbose_name = _('Bài viết')
        verbose_name_plural = _('Bài viết')
        permissions = [
            ("can_approve_article", "Can approve Bài viết"),
        ]
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or str(self.id)
    
    def save(self, *args, **kwargs):
        self.slug = create_slug(self.safe_translation_getter('name', language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE))
        super().save(*args, **kwargs)
    
    @admin.display(description=_('Hình ảnh'))
    def get_image_count(self):
        return self.image_article.count()
    
    @admin.display(description=_('Tài liệu'))
    def get_document_count(self):
        return self.document_article.count()

    @admin.display(description=_('Đường dẫn ngoài'))
    def get_link_count(self):
        return self.link_article.count()
    

class Image(BaseModel):
    thumbnail = ResizedImageField( upload_to=upload_to, max_length=1000, null=True, blank=True, verbose_name=_("Ảnh thu nhỏ"))
    file = models.ImageField(upload_to=upload_to, max_length=1000, verbose_name=_("Ảnh đầy đủ"))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="image_article")

    class Meta:
        ordering = ['order', 'created_at']
        db_table = f'tb_{app_label}_image'
        verbose_name = _('Hình ảnh')
        verbose_name_plural = _('Hình ảnh')


class Document(BaseTranslatableModel):
    translations = TranslatedFields(
        file = models.FileField(upload_to=upload_to, max_length=1000, validators=[validate_document_extension], verbose_name=_("Tệp tài liệu"))
    )
    thumbnail = ResizedImageField( upload_to=upload_to, max_length=1000, null=True, blank=True, verbose_name=_("Ảnh thu nhỏ"))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="document_article")

    class Meta:
        ordering = ['order', 'created_at']
        db_table = f'tb_{app_label}_document'
        verbose_name = _('Tài liệu')
        verbose_name_plural = _('Tài liệu')


class Link(BaseTranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_("Tên")),
        link = models.CharField(max_length=1000, verbose_name=_("Liên kết")),
    )
    thumbnail = ResizedImageField( upload_to=upload_to, max_length=1000, null=True, blank=True, verbose_name=_("Ảnh thu nhỏ"))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="link_article")

    class Meta:
        ordering = ['order', 'created_at']
        db_table = f'tb_{app_label}_link'
        verbose_name = _('Liên kết ngoài')
        verbose_name_plural = _('Liên kết ngoài')
        