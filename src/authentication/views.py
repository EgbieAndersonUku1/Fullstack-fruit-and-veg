from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .utils.password_validator import PasswordStrengthChecker
from utils.post_json_validator import validate_json_and_respond
from utils.generator import generate_forgotten_password_url
from .forms.register_form import RegisterForm
from .forms.passwords.forgotten_password import ForgottenPasswordForm
from .forms.passwords.new_password import NewPasswordForm
from .views_helper import send_verification_email
from utils.send_emails_types import (send_registration_email, 
                                      resend_expired_verification_email, 
                                      send_forgotten_password_verification_email
                                      )


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
        
        messages.error(request, "Please correct the errors below.")
    
    return redirect('home')
    
    
def user_login(request):
    """
    Handles user login by validating credentials and managing user feedback based on account status.
    
    This function is designed to be called by a fetch request from the frontend. It uses the `validate_user_login`
    helper function to perform user authentication and then provides appropriate feedback messages to the user
    based on their account status (banned, inactive, or successful login).

    Args:
        request (HttpRequest): The request object containing user credentials. The credentials should be included
                               in the request's POST data, with keys "email" and "password".
    
    Returns:
        bool: True if login is successful, otherwise False. This boolean indicates the success or failure of
              the login process, which can be used by the frontend to display appropriate messages or redirect.
    """
    
    field_name = "auth"

    def validate_user_login(data:dict):
        """
        Validates user login credentials and checks account status.
        
        Args:
            data (dict): Dictionary containing user credentials with keys "email" and "password".
        
        Returns:
            bool: True if the user is authenticated and active, otherwise False.
        """
        
        email    = data.get("email")
        password = data.get("password")
        user     = authenticate(request, email=email, password=password)
        
     
        if user:
            if user.is_banned:
                error_msg = "Your account has been banned, please contact support."
            elif not user.is_active:
                error_msg = "Your account is no longer active, please contact support."
            else:
                messages.success(request, "Welcome back, you have successfully logged in.")
                login(request, user)
                return True, ''
        else:
            error_msg="The username and/or password is invalid."
        
        return False, error_msg

    
    return validate_json_and_respond(request,
                            field_name,
                            follow_up_message='Credentials are valid.',
                            validation_func=validate_user_login,
        
    )



@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def user_logout(request):
    """
    Logouts the user out and clears the session from the browser.
    
    Args:
        request (HttpRequest): The request containing the session

    """
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("home")


def validate_password(request):
    """
    Validates the strength of a password provided in the request.

    This function is called by a fetch request from the frontend to check if the provided password meets 
    the required strength criteria. It uses the `password_strength_checker` helper function to assess 
    the password's strength and provides appropriate feedback based on the validation result.

    Args:
        request (HttpRequest): The request object containing the password to be validated. The password should 
                               be included in the request's POST data with the key "password".

    Returns:
        bool: True if the password is strong according to the defined criteria, otherwise False. This boolean 
              value indicates whether the password is considered strong or not, which can be used by the 
              frontend to display validation messages or prompt the user to choose a stronger password.
    """
    
    field_name = "password"
    error_msg  = f"{field_name.title()} is in use"
    
    def password_strength_checker(password):
        checker = PasswordStrengthChecker(password)  
        return checker.is_strong_password(), error_msg

    return validate_json_and_respond(request, field_name, follow_up_message='Password is valid', 
                           validation_func=password_strength_checker)


def validate_email(request):
    """
    Validates the uniqueness of an email address provided in the request.

    This function is called by a fetch request from the frontend to check if the provided email address is 
    unique and not already in use by another user. It uses the `is_email_unique` helper function to check
    the email's uniqueness and provides appropriate feedback based on the validation result.

    Args:
        request (HttpRequest): The request object containing the email address to be validated. The email should
                               be included in the request's POST data with the key "email".

    Returns:
        bool: True if the email is unique (not already in use), otherwise False. This boolean value indicates
              whether the email can be used for registration or needs to be changed, which can be used by the
              frontend to display validation messages or prompt the user to enter a different email address.
    """
    
    field_name = "email"
    error_msg  = f"{field_name.title()} is in use"
    
    def is_email_unique(email):
        return not User.objects.filter(email=email).exists(), error_msg
    
    return validate_json_and_respond(request, field_name, follow_up_message='Email is valid', 
                           validation_func=is_email_unique
                           )


def validate_username(request):
    """
    Validates the uniqueness of a username provided in the request.

    This function is called by a fetch request from the frontend to check if the provided username is unique
    and not already in use by another user. It uses the `is_username_unique` helper function to check
    the username's uniqueness and provides appropriate feedback based on the validation result.

    Args:
        request (HttpRequest): The request object containing the username to be validated. The username should
                               be included in the request's POST data with the key "username".

    Returns:
        bool: True if the username is unique (not already in use), otherwise False. This boolean value indicates
              whether the username can be used for registration or needs to be changed, which can be used by the
              frontend to display validation messages or prompt the user to enter a different username.
    """
    
    field_name = "username"
    error_msg  = f"{field_name.title()} is in use"
    
    def is_username_unique(username):
        return not User.objects.filter(username=username).exists(), error_msg
    
    return validate_json_and_respond(request, field_name, follow_up_message='Username is valid',  
                          validation_func=is_username_unique)



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
    
    user             = User.get_by_username(username)
    VERIFICATION_KEY = "email_verification"
   
    if not user:
        messages.error(request, "The user associated with this code doesn't exist.")
        return redirect("home")
    
    is_valid, status = user.is_verification_code_valid(token, default_key=VERIFICATION_KEY)
    
    # Check if the user is already logged in
    if request.user.is_authenticated and not user.verification_data.get(VERIFICATION_KEY):
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
    
    if is_valid:
        user.mark_email_as_verified(save=False) # don't save yet
        user.clear_verification_data(default_key=VERIFICATION_KEY)
    
        messages.success(request, "You have successfully confirmed your email. You can now log in.")
        return redirect("home")



def forgotten_password(request):
    
    MESSAGE          = "If your email exist a new verification link will be sent to your registered email address"
    VERIFICATION_KEY = "forgotten_password_verification_code"
    
    if request.method == "POST":
        form = ForgottenPasswordForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            user  = User.get_by_email(email)
            
            if user:
                resp = user.is_token_request_allowed()

                if not resp:
                    messages.info(request, "Please wait ten minutes before requestiing a new password")
                else:
                    subject = "Click the verification link to change your password"
                    HOUR_IN_SECS = 3600
                    send_verification_email(request, 
                                            user=user, 
                                            subject=subject, 
                                            follow_up_message=MESSAGE, 
                                            send_func=send_forgotten_password_verification_email,
                                            generate_verification_url_func=generate_forgotten_password_url,
                                            verification_key=VERIFICATION_KEY,
                                            expiry_date=HOUR_IN_SECS,
                                            )
            else:
                messages.success(request, MESSAGE)
            return redirect("home")
         
    else:
        form = ForgottenPasswordForm()
           
    context = {
        "form": form,
    }
    return render(request, "passwords/forgotten_password.html", context=context)


def new_password(request, username, token):
    
    user      = User.get_by_username(username)
    ERROR_MSG = "There is no token associated with that username"
    
    if not user:
        messages.warning(request, ERROR_MSG)
        return redirect("home")
   
    VERIFICATION_KEY = "forgotten_password_verification_code"
    is_valid, status = user.is_verification_code_valid(token, default_key=VERIFICATION_KEY)
    
    if not is_valid:
        messages.error(request, "The token you entered is invalid.")
        return redirect("home")
    
    if status == "EXPIRED":
        # Token has expired, send a new one
        messages.info(request, "The token you entered has expired. A new one has been sent to your email address.")
  
        subject           = "New verification link to change your password"
        HOUR_IN_SECS      = 3600
        follow_up_message = "Another verification token has been sent. Please check your email address."
        
        send_verification_email(request, 
                                user=user, 
                                subject=subject, 
                                follow_up_message=follow_up_message, 
                                send_func=send_forgotten_password_verification_email,
                                generate_verification_url_func=generate_forgotten_password_url,
                                verification_key=VERIFICATION_KEY,
                                expiry_date=HOUR_IN_SECS)
        return redirect("home")
    
    if request.method == "POST":
        
        form = NewPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["new_password"]
            user.set_password(password)
            user.clear_verification_data(default_key=VERIFICATION_KEY)  #  automatically saves since default it set to save
            messages.success(request, "You have successfully changed your password. Please log in using your new password.")
            return redirect("home") 
    else:
        form = NewPasswordForm()

    context = {
        "form": form,
        "username": username,
        "token": token,
    }
    return render(request, "passwords/new_password.html", context=context)


def check_session(request):
    """
    Checks if the user is logged in.

    This function is intended for use with a fetch request. If the user is 
    authenticated, it returns a JSON response indicating `is_logged_in: True`. 
    Otherwise, it returns a JSON response with `is_logged_in: False`.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response with the user's login status.
    """
    if request.user.is_authenticated:
        return JsonResponse({"IS_LOGGED_IN": True}, status=200)
    return JsonResponse({"IS_LOGGED_IN": False}, status=200)

    
        
        