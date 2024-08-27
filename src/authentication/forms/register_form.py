from pyexpat.errors import messages
from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

from ..utils.generator import generate_token
from ..utils.send_emails import send_registration_email


User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "register-password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "register-confirm-password"})
    )
    show_password = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={"id": "show-password"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]

  
   