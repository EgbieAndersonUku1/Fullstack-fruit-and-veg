from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest 
from .models import (
                    ActiveUserProxy,
                    AdminUserProxy,
                    BannedUserProxy,
                    NonActiveUserProxy,
                    StaffUserProxy,
                    SuperUserProxy,
                    User,
                    VerifiedUserProxy
)




class BaseUserAdminReadonlyFields(admin.ModelAdmin):
    readonly_fields = ["password", "email", "username"]
    
    
    
class BaseUserAdmin(admin.ModelAdmin):
    ordering            = ['-date_created']
    list_display        = ('id', 'email', 'username', 'is_superuser', 'is_staff', 'is_active', 'is_email_verified', 'last_login')
    list_display_links  = ("id", "username", "email")
    list_per_page       = 25 
    search_fields       = ('email', 'username')
    
    
class AdminUser(BaseUserAdmin):
    
    class Meta:
         model  = User
         
    list_filter  = ('is_staff', 'is_active', 'is_email_verified', 'is_superuser', 'is_banned')
    
    # Fieldsets define the layout of the form view
    fieldsets = (
        (None, {'fields': ('email', 'username','password' )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_banned', 'user_permissions', 'groups')}),
      
    )

    # Optional: Horizontal filters for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions',)





class AdminVerifiedUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the VerifiedUserProxy model to manage verified users in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have 
    verified their email addresses.
   
    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only users with verified email addresses.
    """
    
    readonly_fields  = ['username', 'last_login', 'password', 'email']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_email_verified=True)



class AdminBannedUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the BannedUserProxy model to manage banned users in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have been banned.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only banned users.
    """
    readonly_fields  = ['username', 'last_login', 'password', 'email']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_banned=True)

        

class AdminSuperUserProxy(BaseUserAdmin):
    """
    Custom admin class for the SuperUserProxy model to manage superusers in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have superuser status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only superusers.
    """
    readonly_fields  = ['username', 'last_login', 'password', 'email']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_superuser=True)



class AdminUserProxyModel(BaseUserAdmin):
    """
    Custom admin class for the AdminUserProx model to manage admin in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have admin status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only superusers.
    """
    readonly_fields  = ['username', 'last_login', 'password', 'email']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_admin=True)




class AdminStaffUserProxy(BaseUserAdmin):
    """
    Custom admin class for the StaffUserProxy model to manage staff in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have staff status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only staff/admin users.
    """
    readonly_fields  = ['username', 'last_login', 'password', 'email']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_staff=True)



class AdminActiveUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the ActiveUserProxy model to manage staff in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have active status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only staff/admin users.
    """
    readonly_fields  = ['username', 'last_login', 'password', 'email']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_active=True)



class AdminNonActiveUserProxy(BaseUserAdmin):
    """
    Custom admin class for the NonActiveUserProxy model to manage staff in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who are no longer
    have active status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only staff/admin users.
    """
    readonly_fields  = ('username', 'last_login', 'password', 'email')
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_active=False)


admin.site.register(ActiveUserProxy, AdminActiveUserProxy)
admin.site.register(AdminUserProxy, AdminUserProxyModel)
admin.site.register(BannedUserProxy, AdminBannedUserProxy)
admin.site.register(NonActiveUserProxy, AdminNonActiveUserProxy)
admin.site.register(SuperUserProxy, AdminSuperUserProxy)
admin.site.register(StaffUserProxy, AdminStaffUserProxy)
admin.site.register(User, AdminUser)
admin.site.register(VerifiedUserProxy, AdminVerifiedUserProxy)
