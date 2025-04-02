from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_app.forms import CustomUserCreationForm
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets=(
        (
            'Individuelle Daten',
            {
                'fields':(
                    'custom',
                    'phone',
                    'address'
                )
            }
        ),
        *UserAdmin.fieldsets,
    )