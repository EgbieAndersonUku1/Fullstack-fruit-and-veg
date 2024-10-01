from django import forms 

from user_profile.models import BillingAddress, UserProfile, ShippingAddress

from utils.country_parser import parse_country_file



class PrimaryAddress:
    YES = '1'
    NO  = '2'
    CHOICES = [(YES, 'Yes'), (NO, 'No')]
    
    
    
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = "__all__"


class BillingAddressForm(forms.ModelForm):
    
    class Meta:
        model = BillingAddress
        fields = ["country", "address_1", "city", "state", "postcode"]
    
    is_primary_address = forms.ChoiceField(choices=PrimaryAddress.CHOICES, widget=forms.RadioSelect, initial=PrimaryAddress.YES)



class ShippingAddressForm(forms.ModelForm):
    
    # These shipping address fields are set to not required (required=False) because they are hidden from view
    # when the form is displayed alongside the billing form. This configuration ensures that the form 
    # can still be submitted even if these fields are left empty when only the billing form is completed.
    address_1          = forms.CharField(required=False)
    city               = forms.CharField(required=False)
    state              = forms.CharField(required=False)
    postcode           = forms.CharField(required=False)
  
    class Meta:
        model = ShippingAddress
        fields = ["country", "address_1", "city", "state", "postcode"]

