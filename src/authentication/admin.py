from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from authentication.forms.ban_user_form import BanUserAdminForm

from .models import (
                    ActiveUserProxy,
                    AdminUserProxy,
                    BanUser,
                    BannedUserProxy,
                    NonActiveUserProxy,
                    StaffUserProxy,
                    SuperUserProxy,
                    User,
                    UserDevice,
                    UserBaseLineData,
                    VerifiedUserProxy,
                    TempBannedUserProxy
)


class BaseUserAdminReadonlyFields(admin.ModelAdmin):
    readonly_fields = ["password", "email", "username", "verification_data"]


class BaseUserAdmin(admin.ModelAdmin):
    ordering            = ['-date_created']
    list_display        = ('id', 'email', 'username', 'is_superuser', 'is_staff', 'is_active', 'is_email_verified', 'last_login')
    list_display_links  = ("id", "username", "email")
    list_per_page       = 25 
    search_fields       = ('email', 'username')
    
    
class AdminUser(BaseUserAdmin, BaseUserAdminReadonlyFields):
    
    class Meta:
         model  = User
         
    list_filter  = ('is_staff', 'is_active', 'is_email_verified', 'is_superuser')
    
    
    # Fieldsets define the layout of the form view
    fieldsets = (
        (None, {'fields': ('email', 'username','password' )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'user_permissions', 'groups')}),
      
    )

    readonly_fields = ("verification_data", )
    
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
   
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_banned=True)


class AdminBTempBannedUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the BannedUserProxy model to manage banned users in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have been banned.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only banned users.
    """
   
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_temp_ban=True)
    
    
class AdminSuperUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the SuperUserProxy model to manage superusers in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have superuser status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only superusers.
    """
  
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_superuser=True)



class AdminUserProxyModel(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the AdminUserProx model to manage admin in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have admin status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only superusers.
    """
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_admin=True)




class AdminStaffUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the StaffUserProxy model to manage staff in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who have staff status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only staff/admin users.
    """
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
    readonly_fields  = ['username', 'last_login', 'password', 'email', 'last_token_generated_on']
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_active=True)



class AdminNonActiveUserProxy(BaseUserAdmin, BaseUserAdminReadonlyFields):
    """
    Custom admin class for the NonActiveUserProxy model to manage staff in the Django admin interface.

    This class extends the functionality of the BaseUserAdmin to display only users who are no longer
    have active status.

    Methods
    -------
    get_queryset(request: HttpRequest) -> QuerySet[Any]
        Returns a queryset filtered to include only staff/admin users.
    """
  
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query_set = super().get_queryset(request)
        return query_set.filter(is_active=False)



class UserBanAdmin(admin.ModelAdmin):
    
    list_display       = ["id", "user", "username", "start_date", "expires_on", "ban_duration_days", "remaining_days"]
    readonly_fields    = ['modified_on']
    list_display_links = ["id", "user"]
 
    form = BanUserAdminForm
    
    def username(self, obj):
        return obj.username
    
    def start_date(self, obj):
        return obj.ban_start_date if obj.ban_start_date else "N/A"

    def expires_on(self, obj):
        return obj.ban_expires_on if obj.ban_expires_on else "N/A"
  
        
    def ban_duration_days(self, obj):
        ban_duration = obj.ban_duration_days
        return "Permanent Ban" if ban_duration == None else ban_duration
    
    def remaining_days(self, obj):
        remaining_days = obj.remaining_days
        return "Permanent Ban" if remaining_days == None else remaining_days

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)




class UserDeviceAdmin(admin.ModelAdmin):
    
    list_display        = ["id", "user", "platform", "last_login", "created_on", "modified_on"]
    list_display_links  = ["id", "platform"]
    list_filter         = ["is_touch_device"]
    list_per_page       = 25
    search_fields       = ["id", "local_ip", "platform"]
    readonly_fields     = ["last_login", "created_on", "modified_on", "local_ip"]
    
    # Fieldsets define the layout of the form view
    fieldsets = (
        (None, {'fields': ('user', 'local_ip', 'user_agent', 'platform', "device" )}),
        ('Timezones', {'fields': ('frontend_timezone',)}),
        ('Browser', {'fields': ('browser', 'browser_version')}),
        ('Screen size', {'fields': ('screen_width', 'screen_height')}),
        ('Additional information', {'fields': ('pixel_ratio', 'is_touch_device', 'last_login', 'created_on', 'modified_on')}),
      
    )


class BaseLineDataAdmin(admin.ModelAdmin):
    list_display        = ["id", "user", "country", "hostname", "created_on", "modified_on"]
    list_display_links  = ["id", "country"]
    list_filter         = ["is_successful"]
    list_per_page       = 25
    search_fields       = ["id", "client_ip_address", "country", "region", "latitude", "longitude"]
    readonly_fields     = ["is_successful", "created_on", "modified_on"]
    
    # Fieldsets define the layout of the form view
    fieldsets = (
        (None, {'fields': ('user', 'client_ip_address', 'hostname', 'organization', 'country', 'region', )}),
        ('Coordinates', {'fields': ('latitude', 'longitude')}),
        ('Additional information', {'fields': ('timezone', 'created_on', 'modified_on')}),
      
    )



class UserBaseLineDataAdmin(BaseLineDataAdmin):
   pass
    

admin.site.register(ActiveUserProxy, AdminActiveUserProxy)
admin.site.register(AdminUserProxy, AdminUserProxyModel)
admin.site.register(BannedUserProxy, AdminBannedUserProxy)
admin.site.register(BanUser, UserBanAdmin)
admin.site.register(NonActiveUserProxy, AdminNonActiveUserProxy)
admin.site.register(SuperUserProxy, AdminSuperUserProxy)
admin.site.register(StaffUserProxy, AdminStaffUserProxy)
admin.site.register(TempBannedUserProxy, AdminBTempBannedUserProxy)
admin.site.register(User, AdminUser)
admin.site.register(VerifiedUserProxy, AdminVerifiedUserProxy)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(UserBaseLineData, UserBaseLineDataAdmin)