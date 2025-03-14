from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import (
                        Article,
                        Document,
                        Image,
                        Link
                    )
from backend.custom.serializers import BaseSerializer, BaseTranslatableSerializer


# Create your serializers here.

app_label = __name__.split('.')[0]


# Image

class ImageSerializer(BaseSerializer):
    class Meta:
        model = Image
        ref_name = app_label
        fields = [
            'thumbnail',
            'file',
            'article'
        ] + BaseSerializer.base_fields


class ImageOverviewSerializer(BaseSerializer):
    class Meta:
        model = Image
        ref_name = app_label
        fields = [
            'thumbnail',
            'file',
            'article'
        ] + BaseSerializer.base_overview_fields


# Document

class DocumentSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=Document)
    
    class Meta:
        model = Document
        ref_name = app_label
        fields = [
            'translations',
            'thumbnail',
            'article'
        ] + BaseSerializer.base_fields
    

class DocumentOverviewSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=Document)
    
    class Meta:
        model = Document
        ref_name = app_label
        fields = [
            'translations',
            'thumbnail',
            'article'
        ] + BaseSerializer.base_overview_fields


# Link

class LinkSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=Link)

    class Meta:
        model = Link
        ref_name = app_label
        fields = [
            'translations',
            'thumbnail',
            'article'
        ] + BaseSerializer.base_fields


class LinkOverviewSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=Link)

    class Meta:
        model = Link
        ref_name = app_label
        fields = [
            'translations',
            'thumbnail',
            'article'
        ] + BaseSerializer.base_overview_fields


# Article

class ArticleSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=Article)
    image_article = ImageSerializer(many=True)
    document_article = DocumentSerializer(many=True)
    link_article = LinkSerializer(many=True)

    class Meta:
        model = Article
        ref_name = app_label
        fields = [
            'translations',
            'thumbnail',
            'view',
            'like',
            'approve',
            'image_article',
            'document_article',
            'link_article'
        ] + BaseSerializer.base_fields


class ArticleOverviewSerializer(BaseTranslatableSerializer):
    translations = TranslatedFieldsField(shared_model=Article)

    class Meta:
        model = Article
        ref_name = app_label
        fields = [
            'translations',
            'thumbnail',
            'view',
            'like',
            'approve'
        ] + BaseSerializer.base_overview_fields
    