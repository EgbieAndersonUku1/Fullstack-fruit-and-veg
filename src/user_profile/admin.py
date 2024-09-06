from types import NoneType
from django.contrib import admin
from django.forms import BaseInlineFormSet


from .models import ShippingAddress, BillingAddress, UserProfile, GiftCard
from .forms.gift_card_form import IssueGiftCardForm


# Register your models here.

class BaseAddressAdmin(admin.ModelAdmin):
    
    ordering           = ["-date_created"]
    list_display       = ["id", "country", "address_1", "city", "postcode", "user"]
    list_filter        = ["city", "user"]
    search_fields      = ["city", "address_1", "postcode", "country"]
    list_display_links = ["id", "address_1"]
    list_per_page      = 30


class ShippingAddressAdminModel(BaseAddressAdmin):
    pass


class BillingAddressAdminModel(BaseAddressAdmin):
    pass



class GiftCardFormAdmin(admin.ModelAdmin):
    
    form          = IssueGiftCardForm
    ordering      = ["-date_created"]
    list_display  = ['username', 'card_type', 'code', 'value', 'is_active', 'expiration_date', 'does_not_expire']
    list_filter   = ["user_profile", "is_active", "does_not_expire"]
    search_fields = ["user_profile"]
    list_per_page = 50
    
    def username(self, obj):
        if isinstance(obj, GiftCard):
            try:
                return obj.user_profile.user.username
            except (AttributeError, TypeError):
                return "No username found"
    
    username.short_description = "Gift card for user"
    
    def save_related(self, request, form, formsets, change):
      
        
       # The IssueGiftCardForm is a custom form used in the admin to issue gift cards.
       # Normally, Django's admin expects many-to-many (M2M) relationships when saving related forms.
       # Since this form doesn't use M2M fields, the default behaviour is overriding to prevent errors.
       # This avoids M2M errors and ensures the related formsets are handled properly. 
        for formset in formsets:
            if isinstance(formset, BaseInlineFormSet):
                for form in formset.forms:
                    if hasattr(form, 'save_m2m'):
                        form.save_m2m()
    
   

class UserProfileAdmin(admin.ModelAdmin):
    
    ordering      = ["-date_created"]
    list_display  = ['id', 'username', 'email', 'first_name', 'last_name', 'mobile', "num_of_gift_cards", "date_created"]
    list_filter   = ['id', 'first_name', 'last_name', 'mobile']
    search_fields = ['id', 'first_name', 'last_name', 'mobile']
    
    list_per_page  = 30
    
    def full_name(self, obj):
        return obj.full_name
    
    def username(self, obj):
        return obj.username
    
    def email(self, obj):
        return obj.user.email
    
    def num_of_gift_cards(self, obj):
        return obj.num_of_gift_cards
    
    
    full_name.short_description = "Full name"
    email.short_description     = "Email"
    num_of_gift_cards.short_description = "Num of gift cards"
    


admin.site.register(ShippingAddress, ShippingAddressAdminModel)
admin.site.register(BillingAddress, BillingAddressAdminModel)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GiftCard, GiftCardFormAdmin)
