from django import forms


class BaseForm(forms.Form):
    new_password      = forms.CharField(max_length=40, widget=forms.PasswordInput())
    confirm_password  = forms.CharField(max_length=40, widget=forms.PasswordInput())