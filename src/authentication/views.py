
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .utils.password_validator import PasswordStrengthChecker
from .views_helper import validate_helper

from .forms.register_form import RegisterForm
from .views_helper import send_verification_email
from .utils.send_emails_types import send_registration_email, resend_expired_verification_email



# Create your views here.

User = get_user_model()

def register(request):
  
    form = RegisterForm()
    
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            
            subject           = "Please verify your email address"
            follow_up_message = "An email verification email has been sent. Please verify your email address."
            send_verification_email(request, user, subject, follow_up_message, send_registration_email)
         
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
        return not User.objects.filter(email=email).exists() # Note to self change to use the model version
    return validate_helper(request, 'email', 'Email is valid', is_email_unique)


def validate_username(request):
   
    def is_username_unique(username):
        return not User.objects.filter(username=username).exists() # Note to self change to use the model version
    return validate_helper(request, 'username', 'Username is valid',  is_username_unique)



def verify_email_token(request, username, token):
    """
    Verifies the email token for a user and handles different verification scenarios.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - username (str): The username of the user whose email is being verified.
    - token (str): The verification token sent to the user's email.

    Returns:
    - HttpResponseRedirect: Redirects to the home page with appropriate messages.
    """
    
    user = User.get_by_username(username)
   
    if not user:
        messages.error(request, "The user associated with this code doesn't exist.")
        return redirect("home")
    
    is_valid, status = user.is_verification_code_valid(token)
    
    # Check if the user is already logged in
    if request.user.is_authenticated and not user.verification_data:
        messages.info(request, "You have already confirmed your email.")
        return redirect("home")
    
   
    # Validate the verification token
    if not is_valid:
        messages.error(request, "The token you entered is invalid.")
        return redirect("home")
    
    if status == "EXPIRED":
        
        # Token has expired, send a new one
        messages.info(request, "The token you entered has expired. A new one has been sent to your email address.")
  
        subject           = "Please verify your email address"
        follow_up_message = "Another verification token has been sent. Please verify your email address."
        send_verification_email(request, user, subject, follow_up_message, resend_expired_verification_email)
        return redirect("home")
    
    # Token is valid, mark email as verified
    if is_valid:
        user.mark_email_as_verified()
        user.clear_verification_data()
    
        messages.success(request, "You have successfully confirmed your email. You can now log in.")
        return redirect("home")
