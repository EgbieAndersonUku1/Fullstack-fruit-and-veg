from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "register-password",
        
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "register-confirm-password",
        
    }))
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]
    

    def save(self, commit=True):
        pass