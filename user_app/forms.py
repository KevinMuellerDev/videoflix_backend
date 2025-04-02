from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

#Write here aour Custom forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields = '__all__'
