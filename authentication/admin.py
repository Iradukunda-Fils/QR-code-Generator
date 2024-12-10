from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'country', 'role', 'is_active', 'is_admin', 'is_superuser', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_admin', 'is_staff', 'role', 'country')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Update fieldsets for better admin UI
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture', 'phone_number', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'role')}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )
    
    # Improve 'add' fieldset for user creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'country', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    # Optional: Add additional options for displaying timestamps in 'list_display'
    readonly_fields = ('created_at', 'updated_at')  # Make timestamps read-only

    def has_add_permission(self, request):
        return super().has_add_permission(request)  # Custom permission check if needed

