from django.contrib import admin


from .models import ShippingAddress, BillingAddress, UserProfile, GiftCard

# Register your models here.


class BaseAddressAdmin(admin.ModelAdmin):
    ordering           = ["-date_created"]
    list_display       = ["id", "country", "address_1", "city", "postcode", "user"]
    list_filter        = ["city"]
    list_display_links = ["id", "address_1"]
    list_per_page      = 30



class ShippingAddressAdminModel(BaseAddressAdmin):
    pass


class BillingAddressAdminModel(BaseAddressAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    ordering           = ["-date_created"]
    list_display       = ["id", "first_name", "last_name", "telephone", "mobile", "user"]
    list_display_links = ["id", "first_name", "last_name"]
    list_per_page      = 30



class GiftCardAdmin(admin.ModelAdmin):
     ordering   = ["-date_created"]
     list_display = ["id", "name", "code", "is_active", "expiration_date", "value"]
     list_display_links = ["id", "code"]
     list_per_page = 50
    

admin.site.register(ShippingAddress, ShippingAddressAdminModel)
admin.site.register(BillingAddress, BillingAddressAdminModel)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GiftCard, GiftCardAdmin)