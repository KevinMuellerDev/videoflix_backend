import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestCheckUserExists:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return get_user_model().objects.create_user(
            email="test@example.com", password="strongpassword"
        )

    def test_email_exists(self, client, user):
        response = client.get("/check-email/", {"email": "test@example.com"})
        assert response.status_code == 200
        assert response.data["exists"] is True

    def test_email_does_not_exist(self, client):
        response = client.get("/check-email/", {"email": "nonexistent@example.com"})
        assert response.status_code == 200
        assert response.data["exists"] is False

    def test_email_missing(self, client):
        response = client.get("/check-email/")
        assert response.status_code == 400
        assert response.data["error"] == "Email erforderlich"
