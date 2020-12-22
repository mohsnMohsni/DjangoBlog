from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    ordering = ('email',)
    add_fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password1', 'password2')}),
    )
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password')}),
        ('Personal Option', {'fields': ('avatar',)}),
        ('Status', {'fields': ('is_staff', 'is_active', 'groups')})
    )
