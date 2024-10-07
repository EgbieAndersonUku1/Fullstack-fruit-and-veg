from django import forms

class ForgottenPasswordForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=60, widget=forms.EmailInput(
        attrs={
            "Placeholder": "Enter your email adress..."
        }
    ))