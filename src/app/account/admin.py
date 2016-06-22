from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
)

User = settings.AUTH_USER_MODEL


class UserCreationForm(DjangoUserCreationForm):
    """
    Custom user creation form.
    See https://code.djangoproject.com/ticket/19353
    """
    class Meta(DjangoUserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError(
                self.error_messages['duplicate_username']
            )


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """User admin with nicer fieldset."""
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_password_reset')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'email', 'employee_id',
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'username', 'email',
        'first_name', 'last_name',
        'is_staff', 'is_password_reset',
    )
