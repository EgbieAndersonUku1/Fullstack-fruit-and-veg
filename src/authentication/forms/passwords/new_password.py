from typing import Any
from django import forms

from .base_form import BaseForm
from authentication.utils.password_validator import PasswordStrengthChecker


class NewPasswordForm(BaseForm):
  
    def clean_new_password(self) -> dict[str, Any]:
        
        password           = self.cleaned_data.get("new_password")
        password_validator = PasswordStrengthChecker(password)
        
        if not password_validator.contains_at_least_length_chars():
            raise forms.ValidationError("The password must contain at least eight characters")
        
        if not password_validator.contains_at_least_one_number():
            raise forms.ValidationError("The password must contain at least one number")
        
        if not password_validator.contains_lowercases():
            raise forms.ValidationError("The password must contain at least one lowercase")
        
        if not password_validator.contains_uppercases():
            raise forms.ValidationError("The password must contain at least one uppercase")
        
        if not password_validator.contains_special_chars():
            raise forms.ValidationError("The password must contain at least one special character")
        
        if not password_validator.is_strong_password():
            raise forms.ValidationError("The password provided is not a strong password")

        return password
    
    def clean(self):
        cleaned_data = super().clean()
        
        password         = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and confirm_password != password:
            raise forms.ValidationError("The passwords does not match")
        return cleaned_data
    
    
