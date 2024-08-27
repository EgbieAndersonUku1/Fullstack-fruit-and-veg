import json
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .utils.password_validator import PasswordStrengthChecker
from .views_helper import validate_helper

from .forms.register_form import RegisterForm
from .utils.generator import generate_token, generate_verification_url
from .utils.send_emails import send_registration_email



# Create your views here.

User = get_user_model()

def register(request):
  
    form = RegisterForm()
    
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            
            token             = generate_token()
            expiry_minutes    = 4320   # Expires in 3 days
            
            user.set_password(form.cleaned_data["password"])
            user.set_verification_code(token, expiry_minutes)
            user.save()
            
            # Generate the verification URL dynamically using request
            verification_url = generate_verification_url(request, user)
            
            send_registration_email(subject="Please verify your email address",
                                    from_email=settings.EMAIL_HOST_USER,
                                    user=user,
                                    verification_url=verification_url,
                                    )
            
            messages.success(request, "You have successfully registered")
            messages.success(request, "Please verify your email address")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    
    return redirect('home')
    
    
def validate_password(request):
    def password_strength_checker(password):
        checker = PasswordStrengthChecker(password)
        return checker.is_strong_password()

    return validate_helper(request, 'password', 'Password is valid', password_strength_checker)


def validate_email(request):
    def is_email_unique(email):
        return not User.objects.filter(email=email).exists()
    return validate_helper(request, 'email', 'Email is valid', is_email_unique)


def validate_username(request):
   
    def is_username_unique(username):
        return not User.objects.filter(username=username).exists()
    return validate_helper(request, 'username', 'Username is valid',  is_username_unique)



def verify_email(request, username, token):
    pass