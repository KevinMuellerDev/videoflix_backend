import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError
from user_app.serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer,
    CustomPasswordResetConfirmSerializer
)

User = get_user_model()

@pytest.mark.django_db
class TestCustomUserSerializers:

    def test_user_create_serializer_valid(self):
        """Testet, ob ein Benutzer korrekt über den Serializer erstellt wird."""
        data = {
            "email": "test@example.com",
            "password": "securepassword",
            "custom": "Custom Info",
            "phone": "1234567890",
            "address": "Teststraße 1"
        }

        serializer = CustomUserCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.email == "test@example.com"
        assert user.username == "test@example.com"  # wird im Modell beim Speichern gesetzt
        assert user.custom == "Custom Info"
        assert user.phone == "1234567890"
        assert user.address == "Teststraße 1"
        assert user.check_password("securepassword")

    def test_user_create_serializer_invalid_email(self):
        """Testet, ob ungültige E-Mail fehlschlägt."""
        data = {
            "email": "",
            "password": "securepassword"
        }

        serializer = CustomUserCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_user_serializer_output(self):
        """Testet, ob CustomUserSerializer korrekte Felder liefert"""
        user = User.objects.create_user(
            email="visible@example.com",
            password="pw",
            custom="Test",
            phone="12345",
            address="Main Street"
        )

        serializer = CustomUserSerializer(user)
        data = serializer.data

        assert data["email"] == "visible@example.com"
        assert data["custom"] == "Test"
        assert data["phone"] == "12345"
        assert data["address"] == "Main Street"
        assert "password" not in data  # darf nicht enthalten sein

    def test_password_reset_confirm_serializer_valid_integration(self):
        """
        Integrationstest für PasswordResetConfirmSerializer:
        - Erzeugt echten User
        - Generiert gültigen uid/token
        - Testet Passwortänderung über Serializer
        """
        user = User.objects.create_user(
            email="test@example.com",
            password="old_password123"
        )
    
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
    
        data = {
            "uid": uid,
            "token": token,
            "new_password": "new_secure_pass123",
            "confirm_password": "new_secure_pass123"
        }
    
        factory = APIRequestFactory()
        request = factory.post("/fake-url/")
    
        class FakeView:
            token_generator = default_token_generator
    
        context = {
            "request": Request(request),
            "view": FakeView()
        }
    
        serializer = CustomPasswordResetConfirmSerializer(data=data, context=context)
        assert serializer.is_valid(raise_exception=True)
    
        serializer.save()
        user.refresh_from_db()
        assert user.check_password("new_secure_pass123")

    def test_password_reset_confirm_serializer_mismatch(self):
        """Testet, ob bei Passwort-Mismatch ein Fehler geworfen wird"""
        data = {
            "uid": "fakeuid123",
            "token": "faketoken456",
            "new_password": "testpass123",
            "confirm_password": "differentpass"
        }

        serializer = CustomPasswordResetConfirmSerializer(data=data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)

        assert "Passwords do not match." in str(excinfo.value)
