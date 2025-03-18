from import_export import resources, fields
from django.conf import settings

from .models import User


# Create your models here.

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'gender', 'birth', 'address', 'bio', 'public', 'is_active', 'is_staff', 'is_superuser')
