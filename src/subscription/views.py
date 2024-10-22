import json


from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.db import IntegrityError

from utils.post_json_validator import validate_json_and_respond
from utils.validator import validate_email
from .models import NewsletterSubscription


# Create your views here.
User = get_user_model()


@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def subscribe_user(request):
    
    field_name = "subscription"
    
    def subscribe(data:dict):
        
        
        email     = data.get("email", "")
        is_valid  = False
        error_msg = None
        
        if not email:
            error_msg = "The email field cannot be empty"
            return is_valid, error_msg
        
        if not validate_email(email):
             error_msg = "The email has an invalid format"
             return is_valid, error_msg
            
        user  = request.user
        try:
            NewsletterSubscription.objects.create(user=user, email=email)
        except IntegrityError:
            error_msg = "There is a user that has been subscribed using that email"
        else:
            is_valid = True
            error_msg = ""
        return is_valid, error_msg
    
    return validate_json_and_respond(request=request, 
                                     field_name=field_name,
                                     follow_up_message="Successfully subscribed",
                                     validation_func=subscribe
                                     )
        
        
        

