from django import forms


#  aria-required="true"
#   aria-describedby="email-description"
class LoginForm(forms.Form):
    
    email = forms.EmailField(label="Email", 
                             max_length=80, 
                             widget=forms.EmailInput(attrs={
                                 "id": "login-email",
                                 "aria-required": "true",
                                 "aria-describedBy": "email-description",
                             }))
    
    password = forms.CharField(label="Password", max_length=40, 
                               widget=forms.PasswordInput(attrs={
                                   "id": "login-password",
                                    "aria-required": "true",
                                    "aria-describedBy": "password-description",
                                   
                               }))