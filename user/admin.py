from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your custom user model
from django.urls import reverse

# Define a custom user admin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')  # Fields to display in the user list
    list_filter = ('is_active', 'is_staff', 'is_superuser')  # Filters in the sidebar
    search_fields = ('email', 'first_name', 'last_name')  # Searchable fields
    ordering = ('email',)  # Default ordering for the user list

    def get_redirect_url(self, request, obj):
        if obj:
            return reverse('admin:user_customuser_change', args=[obj.pk])
        return reverse('admin:user_customuser_changelist')

    # Fields to be displayed when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff')}
        ),
    )

    # Make sure to use the custom user model
    def save_model(self, request, obj, form, change):
        obj.save()

# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)