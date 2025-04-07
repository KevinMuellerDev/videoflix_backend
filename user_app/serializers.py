from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'password', 'username', 'custom', 'phone', 'address')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': False, 'allow_blank': True},
            'custom': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
        }

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'custom', 'phone', 'address')
