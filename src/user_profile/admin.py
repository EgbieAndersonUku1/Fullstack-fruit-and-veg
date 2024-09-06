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


class UserProfileAdmin(admin.ModelAdmin):
    ordering           = ["-date_created"]
    list_display       = ["id", "first_name", "last_name", "telephone", "mobile", "user"]
    list_display_links = ["id", "first_name", "last_name"]
    search_fields      = ["id", "first_name", "last_name", "telephone", "mobile"]
    list_per_page      = 30


class GiftCardFormAdmin(admin.ModelAdmin):
    
    
    form = IssueGiftCardForm
    ordering = ["-date_created"]
    list_display = ['card_type', 'user', 'code', 'value', 'is_active', 'expiration_date', 'does_not_expire']
    list_filter  = ["user", "is_active", "does_not_expire"]
    search_fields = ["user"]
   
    list_per_page = 50
    
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
    
   




    
  
    

admin.site.register(ShippingAddress, ShippingAddressAdminModel)
admin.site.register(BillingAddress, BillingAddressAdminModel)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GiftCard, GiftCardFormAdmin)
