from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email as the username.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)  # Setzt username gleich email
        user.set_password(password)
        user.save(using=self._db)
        return user

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    custom = models.CharField(max_length=500,default='')
    phone = models.CharField(max_length=12, default='')
    address = models.CharField(max_length=150, default='')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email
        super(CustomUser, self).save(*args, **kwargs)