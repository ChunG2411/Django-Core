from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields
from django_resized import ResizedImageField
from django.contrib.auth.models import Permission
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
import uuid

from backend.custom.models import BaseModel, BaseTranslatableModel, BaseIDModel, BaseCreateModel, BaseUpdateModel, BaseDeleteModel
from backend.custom.functions import upload_to, create_slug
from .managers import CustomUserManager


# Create your models here.

app_label = __name__.split('.')[0]
GENDER = [
    ('1', 'Male'),
    ('2', 'Female'),
    ('3', 'Other')
]

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


class User(
            BaseIDModel,
            BaseCreateModel,
            BaseUpdateModel,
            BaseDeleteModel,
            AbstractUser
        ):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('Tên người dùng'), max_length=100, unique=True, validators=[username_validator])
    email_validator = validators.validate_email
    email = models.EmailField(_('Thư điện tử'), unique=True, validators=[email_validator])
    email_verified = models.BooleanField(default=False)
    phone = models.CharField(_('Số điện thoại'), max_length=12, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)

    first_name = models.CharField(_('Họ'), max_length=100)
    last_name = models.CharField(_('Tên'), max_length=100)
    gender = models.CharField(_('Giới tính'), max_length=10, choices=GENDER, null=True, blank=True)
    birth = models.DateField(_('Sinh nhật'), null=True, blank=True)
    address = models.CharField(_('Địa chỉ'), max_length=255, blank=True, null=True)
    avatar = models.ImageField(_('Ảnh đại diện'), upload_to=upload_to, null=True, blank=True)
    bio = models.TextField(_('Mô tả'), null=True, blank=True)
    public = models.BooleanField(_('Công khai'), default=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    
    class Meta:
        ordering = ['date_joined']
        db_table = f'tb_{app_label}_user'
        verbose_name = _('Người dùng')
        verbose_name_plural = _('Người dùng')
    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    @property
    def completed_percent(self):
        fields = ["first_name", "last_name", "address", "phone", "birth", "bio", "avatar", "gender"]
        count_fields = len(fields)
        empty_values = ["", None]
        empty_values_count = 0

        for field in fields:
            field_value = getattr(self, field)
            if field_value in empty_values:
                empty_values_count += 1
        empty_values_percent = (empty_values_count / count_fields) * 100
        completed_fields_percent = 100 - round(empty_values_percent)
        return completed_fields_percent


class VerifyEmail(
                  BaseIDModel,
                  BaseCreateModel,
                  BaseUpdateModel  
                ):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verifyemail_user")
    code = models.CharField(max_length=6)

    class Meta:
        db_table = f'tb_{app_label}_verify_mail'
        verbose_name = _('Mã email')
        verbose_name_plural = _('Mã email')
        