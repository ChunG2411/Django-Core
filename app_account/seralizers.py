from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from django.core.validators import validate_email
from django.contrib.auth.models import Group, Permission

from .models import (
                        APIKey,
                        User
                    )
from backend.custom.serializers import BaseSerializer, BaseTranslatableSerializer, BaseRepSerializer
from backend.custom.functions import check_validate_password, check_validate_phone


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


class UserSerializer(BaseRepSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email_verified', 'phone', 'phone_verified', 'password', 'groups',
                  'first_name', 'last_name', 'full_name', 'address', 'gender', 'birth', 'avatar', 'bio',
                  'public', 'date_joined', 'completed_percent', 'is_active']
        extra_kwargs = {
            'password': {'write_only': 'true'},
            'email_verified': {'read_only': 'true'},
            'phone_verified': {'read_only': 'true'}
        }
    
    def get_groups(self, obj):
        return [i.id for i in obj.groups.all()]

    def create(self, validated_data):
        request = self.context.get('request')
        password = request.data.get('password')
        email = request.data.get('email')
        phone = request.data.get('phone')

        if phone:
            if not check_validate_phone(phone):
                raise serializers.ValidationError("Số điện thoại không hợp lệ")
            
        status, msg = check_validate_password(password)
        if not status:
            raise serializers.ValidationError(msg)
        
        try:
            validate_email(email)
        except:
            raise serializers.ValidationError("Email không hợp lệ")
        
        validated_data["is_active"] = True

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        phone = request.data.get('phone')
        email = request.data.get('email')

        if phone and phone != instance.phone:
            if not check_validate_phone(phone):
                raise serializers.ValidationError("Số điện thoại không hợp lệ")
            validated_data["phone_verified"] = False

        if email and email != instance.email:
            try:
                validate_email(email)
            except:
                raise serializers.ValidationError("Email không hợp lệ")
            validated_data["email_verified"] = False

        for attr, value in validated_data.items():
            if not attr in ['username', 'group']:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserOverviewSerializer(BaseRepSerializer):
    gender = serializers.SerializerMethodField()
    birth = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone',
                  'full_name', 'address', 'gender', 'birth', 'avatar', 'bio',
                  'groups', 'is_active']
        
    def get_groups(self, obj):
        return [i.id for i in obj.groups.all()]

    def get_email(self, obj):
        return obj.email if obj.public else None
    
    def get_gender(self, obj):
        return obj.gender if obj.public else None
    
    def get_birth(self, obj):
        return obj.birth if obj.public else None
    
    def get_phone(self, obj):
        return obj.phone if obj.public else None
    
    def get_address(self, obj):
        return obj.address if obj.public else None
    
    def get_bio(self, obj):
        return obj.bio if obj.public else None


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class GroupOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']