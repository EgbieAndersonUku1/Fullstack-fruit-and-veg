from django import forms 

from user_profile.models import UserProfile, BillingAddress, ShippingAddress


class PrimaryAddress:
    YES = '1'
    NO  = '2'
    CHOICES = [(YES, 'Yes'), (NO, 'No')]
    
    
    
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = "__all__"


class ShippingAddressForm(forms.ModelForm):
    
    address_1          = forms.CharField(required=True)
    city               = forms.CharField(required=True)
    state              = forms.CharField(required=True)
    postcode           = forms.CharField(required=True)
    is_primary_address = forms.ChoiceField(label="Is primary address", 
                                           choices=PrimaryAddress.CHOICES,
                                           widget=forms.RadioSelect,
                                           required=False,
                                           initial=PrimaryAddress.YES)
    
    class Meta:
        model  = ShippingAddress
        fields = ("country", "address_1", "address_2", "city", "state", "postcode")
        
        

class BillingAddressForm(forms.ModelForm):
    address_1       = forms.CharField(required=False)
    city            = forms.CharField(required=False)
    state           = forms.CharField(required=False)
    postcode        = forms.CharField(required=False)
    primary_address = forms.ChoiceField(label="Is primary address", choices=PrimaryAddress.CHOICES,
                                        widget=forms.RadioSelect, 
                                        required=False,
                                        initial=PrimaryAddress.YES)
    
    class Meta:
        model  = BillingAddress
        fields = "__all__"
        
