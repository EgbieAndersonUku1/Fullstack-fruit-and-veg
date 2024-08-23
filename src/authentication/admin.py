from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class AdminUser(BaseUserAdmin):
    model    = User
    ordering = ['-date_created']


    list_display        = ('id', 'email', 'username', 'is_superuser', 'is_staff', 'is_active', 'is_email_verified', 'last_login')
    list_display_links  = ("id", "username", "email")
    list_filter         = ('is_staff', 'is_active', 'is_email_verified', 'is_superuser', 'is_banned')
    list_per_page       = 25 
    readonly_fields     = ('email', 'username', 'last_login')
    search_fields       = ('email', 'username')

    
    # Fieldsets define the layout of the form view
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Personal info', {'fields': ('username', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_banned', 'user_permissions', 'groups')}),
      
    )

    # Optional: Horizontal filters for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.register(User, AdminUser)
