from django import forms


from base_form import BaseForm


class ChangePasswordForm(BaseForm):
    old_password = forms.CharField(max_length=90, widget=forms.PasswordInput())