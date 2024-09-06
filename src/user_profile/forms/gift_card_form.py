from django import forms
from django.contrib.auth import get_user_model

from ..models import GiftCard

User = get_user_model()

class IssueGiftCardForm(forms.ModelForm):
    
    user            = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    card_type       = forms.CharField(max_length=40, required=False)
    expiry_date     = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)  # Using DateInput with HTML5 date picker
    amount          = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    does_not_expire = forms.BooleanField(required=False)

    class Meta:
        model  = GiftCard
        fields = ['user', 'card_type', 'expiry_date', 'amount', 'does_not_expire']
    
    def save(self, commit=True):
    
        # Call the issue_gift_card method to create the gift card    
        gift_card = GiftCard.issue_gift_card(
            user=self.cleaned_data.get('user'),
            card_type=self.cleaned_data.get('card_type'),
            amount=self.cleaned_data.get('amount'),
            expiry_date=self.cleaned_data.get('expiry_date'),
            does_not_expire=self.cleaned_data.get('does_not_expire')
        )
        
        return gift_card
