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
        fields = ["country", "address_1", "address_2", "city", "state", "postcode"]
    
    is_primary_address = forms.ChoiceField(choices=PrimaryAddress.CHOICES, widget=forms.RadioSelect, initial=PrimaryAddress.YES)



class ShippingAddressForm(forms.ModelForm):
  
    class Meta:
        model = ShippingAddress
        fields = ["country", "address_1", "city", "state", "postcode"]
