from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    custom = models.CharField(max_length=500,default='')
    phone = models.CharField(max_length=12, default='')
    address = models.CharField(max_length=150, default='')

