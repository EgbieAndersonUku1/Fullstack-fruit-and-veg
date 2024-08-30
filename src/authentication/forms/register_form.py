from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(strip=True, max_length=40,
        widget=forms.PasswordInput(attrs={"id": "register-password"})
    )
    confirm_password = forms.CharField(
        strip=True,
        max_length=40,
        widget=forms.PasswordInput(attrs={"id": "register-confirm-password"})
    )
    show_password = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={"id": "show-password"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]

  
    def clean(self):
        cleaned_data     = super().clean()
        password         = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and confirm_password != password:
            self.add_error("confirm_password", "The password doesn't match")
        return cleaned_data
        
       
        