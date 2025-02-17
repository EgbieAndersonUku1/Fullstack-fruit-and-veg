
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.utils import timezone

from utils.post_json_validator import validate_json_and_respond
from utils.validator import validate_email_address
from .utils.sessions import set_session

from .models import NewsletterSubscription, NewsletterSubscriptionHistory, SubscriptionMessage
from .form import SubscriptionFeedBackForm
from utils.tasks import notify_admin_of_user_unsubscription, notify_admin_of_new_subscriber
from utils.post_json_validator import validate_json_and_respond


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
            with transaction.atomic():
                new_subscriber = NewsletterSubscription.objects.create(user=user, 
                                                                       email=email, 
                                                                       subscribed_on=timezone.now(),
                                                                       unsubscribed=False,
                                                                       )
            
                # log the subscription action
                NewsletterSubscriptionHistory.objects.create(title="User subscribed to newsletter",
                                                            user=user,
                                                            email=email,
                                                            action="subscribed",
                                                            start_date=new_subscriber.subscribed_on,
                                                            frequency=new_subscriber.frequency,
                                                           
                                                            
                                                            )
                
                
                set_session(request, session_name="email", email=email)
                is_valid, error_msg = True, ''
                
                subject = "Subject: New Subscriber Alert! 🎉"
                notify_admin_of_new_subscriber(subject, user=new_subscriber)
            
        except IntegrityError: 
             error_msg = "There is a user by that email."
             
        return is_valid, error_msg
            
    return validate_json_and_respond(request=request, 
                                     field_name=field_name,
                                     follow_up_message="Successfully subscribed",
                                     validation_func=subscribe
                                     )
        

@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def manage_subscription(request):
    
    subscription_form    = SubscriptionFeedBackForm()
    subscription         = NewsletterSubscription.objects.filter(user=request.user).first()
    RESULT_PER_PAGE      = 25
    latest_history       = subscription.user.subscription_history.order_by("-timestamp").all() if subscription else None
    subscription_history = latest_history or []
    paginator            = Paginator(subscription_history, RESULT_PER_PAGE) 
    page_number          = request.GET.get("page", 1)
    page_obj             = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "form": subscription_form,
    }
    return render(request, "account/subscription/manage_newsletter_subscription.html", context=context)


@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def update_newsletter_frequency(request):
   
   field_name = "frequency"
   
   def update_frequency(data):
       is_valid  = False
       error_msg = ""
       frequency_update = data.get("frequency", "")
       
       if frequency_update:
           
           try:
               with transaction.atomic():
                    frequency_update      = frequency_update.lower()
                    original_subscription = NewsletterSubscription.objects.get(user=request.user)
                    original_frequency    = original_subscription.frequency
                    
                    if original_frequency.lower() != frequency_update:
                            original_subscription.frequency = frequency_update
                            original_subscription.save()  
                            
                            NewsletterSubscriptionHistory.objects.create(
                                title="User updated frequency field",
                                user=request.user,
                                start_date=original_subscription.subscribed_on,
                                email=original_subscription.email,
                                action="subscribed",
                                frequency=frequency_update,
                            )
           except NewsletterSubscription.DoesNotExist:
                return is_valid, error_msg
            
           is_valid = True
           return is_valid, error_msg
       
       error_msg = "Something went wrong and the field couldn't be updated"
       return is_valid, error_msg
      
   return validate_json_and_respond(request, 
                                    field_name, 
                                    follow_up_message="Successfully updated your newsletter",
                                    validation_func=update_frequency
                                    )
   
   
@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def re_subscribe(request):
  
    subscriber = NewsletterSubscription.get_by_user(user=request.user)
    if subscriber:
        subscriber.subscribe()
        NewsletterSubscriptionHistory.objects.create(title="User has re-subscribed",
                                                         user=subscriber.user,
                                                         email=subscriber.email,
                                                         action="re-subscribed",
                                                         start_date=subscriber.subscribed_on,
                                                         frequency=subscriber.frequency,
                                                         )
            
        # notify admin that user has unsubscribed
        subject = "Subject: Subscriber Alert! 🎉"
        notify_admin_of_new_subscriber(subject, user=subscriber)
        messages.success(request, SubscriptionMessage.SUBSCRIBED)
    else:
        messages.error(request, SubscriptionMessage.ERROR_SUBSCRIBING)
    return redirect("manage_subscription")
        
   
   
   
@login_required(login_url=settings.LOGIN_URL, redirect_field_name="next")
def unsubscribe(request):
    
    form  = SubscriptionFeedBackForm()
    
    if request.method == "POST":
        form = SubscriptionFeedBackForm(request.POST)
        if form.is_valid():
            
            subscriber                          = NewsletterSubscription.get_by_user(user=request.user)
            subscriber.reason_for_unsubscribing = form.cleaned_data["reason_for_unsubscribing"]
            subscriber.unsubscribe()
            
            NewsletterSubscriptionHistory.objects.create(title="User has unsubscribed",
                                                         user=subscriber.user,
                                                         email=subscriber.email,
                                                         action="unsubscribed",
                                                         unsubscribed_on=timezone.now(),
                                                         start_date=subscriber.subscribed_on,
                                                         frequency=subscriber.frequency,
                                                         )
            
            # notify admin that user has unsubscribed
            subject = "Alert a user has unsubscribed"
            notify_admin_of_user_unsubscription(subject, user=subscriber)
            messages.success(request, SubscriptionMessage.UNSUBSCRIBED)
    else:
          messages.error(request, SubscriptionMessage.ERROR_UNSUBSCRIBING)
    
    return redirect("manage_subscription")
    