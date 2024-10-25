from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.db import IntegrityError

from utils.post_json_validator import validate_json_and_respond
from utils.validator import validate_email_address
from .utils.sessions import set_session

from .models import NewsletterSubscription, NewsletterSubscriptionHistory
from utils.generator import generate_token
from utils.send_emails_types import notify_admin_of_new_subscriber


# Create your views here.
User = get_user_model()


@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def subscribe_user(request):
    
    field_name = "subscription"
    
    def subscribe(data:dict):
        
        email                = data.get("email", "")
        is_valid, error_msg  = False, None
              
        if not email:
            error_msg = "The email field cannot be empty"
            return is_valid, error_msg
        
        if not validate_email_address(email):
             error_msg = "The email has an invalid format"
             return is_valid, error_msg
            
        user  = request.user
                
        try:
            new_subscriber = NewsletterSubscription.objects.create(user=user, email=email)
            
            # log the subscription action
            NewsletterSubscriptionHistory.objects.create(title="General Newsletter",
                                                          user=user,
                                                          email=email,
                                                          action="subscribe",
                                                          frequency=new_subscriber.frequency,
                                                         )
            set_session(request, session_name="email", email=email)
            is_valid, error_msg = True, ''
            
            subject = "Subject: New Subscriber Alert! 🎉"
            notify_admin_of_new_subscriber(subject, user=new_subscriber)
            
        except IntegrityError: 
             error_msg = "There is a user by that email"
    
        return is_valid, error_msg
            
    return validate_json_and_respond(request=request, 
                                     field_name=field_name,
                                     follow_up_message="Successfully subscribed",
                                     validation_func=subscribe
                                     )
        
        
def manage_subscription(request):
    return render(request, "account/subscription/manage_newsletter_subscription.html")
