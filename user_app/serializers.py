from djoser.serializers import UserCreateSerializer, UserSerializer,PasswordResetConfirmSerializer
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


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return super().validate(attrs)