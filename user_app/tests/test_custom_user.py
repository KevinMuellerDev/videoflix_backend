import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

@pytest.mark.django_db
class TestCustomUser:

    def test_create_user(self):
        """Teste die Erstellung eines normalen Benutzers"""
        user = User.objects.create_user(
            email="user@example.com",
            password="password"
        )

        assert user.email == "user@example.com"
        assert user.username == "user@example.com"  # username sollte die E-Mail sein
        assert user.check_password("password")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        """Teste die Erstellung eines Superusers"""
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword"
        )

        assert superuser.email == "admin@example.com"
        assert superuser.username == "admin@example.com"  # username sollte die E-Mail sein
        assert superuser.check_password("adminpassword")
        assert superuser.is_active is True
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_create_user_without_email(self):
        """Teste die Erstellung eines Benutzers ohne E-Mail (sollte fehlschlagen)"""
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="password")

    def test_create_superuser_without_staff(self):
        """Teste die Erstellung eines Superusers ohne is_staff (sollte fehlschlagen)"""
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpassword",
                is_staff=False
            )

    def test_create_superuser_without_superuser(self):
        """Teste die Erstellung eines Superusers ohne is_superuser (sollte fehlschlagen)"""
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpassword",
                is_superuser=False
            )

    def test_user_username_is_email(self):
        """Teste, ob der Username die E-Mail ist"""
        user = User.objects.create_user(
            email="testuser@example.com",
            password="password"
        )

        assert user.username == user.email  # Username sollte die E-Mail des Benutzers sein

    def test_user_custom_fields(self):
        """Testet die benutzerdefinierten Felder des Benutzers"""
        user = User.objects.create_user(
            email="customuser@example.com",
            password="password",
            custom="Custom Value",
            phone="1234567890",
            address="123 Test Street"
        )

        assert user.custom == "Custom Value"
        assert user.phone == "1234567890"
        assert user.address == "123 Test Street"

