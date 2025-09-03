"""User Related Admin"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    """User Admin Customization"""
    list_display = ['id', 'username', 'first_name', 'middle_name', 'last_name', 'email',
                    'phone_number', 'date_of_birth', 'gender', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'username', 'first_name', 'middle_name',
                   'last_name', 'email', 'phone_number', 'date_of_birth', 'gender']
    search_fields = ['id', 'username', 'first_name', 'middle_name', 'last_name',
                     'email', 'phone_number','date_of_birth', 'gender']
    ordering = ['id']
    list_display_links = ['id', 'username']
    fieldsets = (
        (None, {
            'fields': ('id', 'username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'middle_name', 'last_name', 'photo', 'email',
                       'phone_number', 'date_of_birth','gender')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups','user_permissions', 'status'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )


admin.site.register(User, CustomUserAdmin)
