import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import UserDevice, CustomUser

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserDeviceType(DjangoObjectType):
    class Meta:
        model = UserDevice
        fields = ('id', 'user', 'device_name', 'ip_address', 'location', 'is_verified', 'created_at')

