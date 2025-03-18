from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from parler.managers import TranslatableQuerySet, TranslatableManager
from parler.models import TranslatableModel


user_model = settings.AUTH_USER_MODEL


class IsNotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class IsNotDeletedTranslatableManager(TranslatableManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False)

class IsActiveTranslatableManager(TranslatableManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False)

    
class BaseCreateModel(models.Model):
    class Meta:
        abstract = True
        
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Ngày khởi tạo"))
    created_by = models.ForeignKey(
        user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
        verbose_name=_("Người khởi tạo")
    )


class BaseUpdateModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Ngày cập nhật"))
    updated_by = models.ForeignKey(
        to=user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
        verbose_name=_("Người cập nhật")
    )


class BaseDeleteModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False, verbose_name=_("Xóa"))
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Ngày xóa")
    )
    deleted_by = models.ForeignKey(
        to=user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_deleted",
        on_delete=models.SET_NULL,
        verbose_name=_("Nguời xóa")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Hoạt động"))

    objects = IsNotDeletedManager()
    objects_active = IsActiveManager()
    objects_all = models.Manager()


class BaseTranslatableDeleteModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False, verbose_name=_("Xóa"))
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Ngày xóa")
    )
    deleted_by = models.ForeignKey(
        to=user_model,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_deleted",
        on_delete=models.SET_NULL,
        verbose_name=_("Nguời xóa")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Hoạt động"))

    objects = IsNotDeletedTranslatableManager()
    objects_active = IsActiveTranslatableManager()
    objects_all = TranslatableManager()


class BaseCustomModel(models.Model):
    class Meta:
        abstract = True

    order = models.IntegerField(null=True, blank=True, verbose_name=_("Thứ tự hiển thị"))
    slug = models.SlugField(null=True, blank=True, max_length=1000, verbose_name=_("Slug"))


class BaseIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name=_("ID"))


class BaseModel(
                BaseIDModel,
                BaseCreateModel,
                BaseUpdateModel,
                BaseDeleteModel,
                BaseCustomModel
            ):
    class Meta:
        abstract = True



class BaseTranslatableModel(
                            BaseIDModel,
                            BaseCreateModel,
                            BaseUpdateModel,
                            BaseTranslatableDeleteModel,
                            BaseCustomModel,
                            TranslatableModel
                        ):
    class Meta:
        abstract = True


