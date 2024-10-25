from .models import NewsletterSubscription
from .utils.sessions import set_session, get_session


def get_subscription_session(request) -> dict:
    """
    A context processor that allows access to the user's newsletter 
    subscription status in any template.
    
    Returns a dictionary containing the user's subscription session.
    """
    subscription_session = None
    try:
        
        # get only unsubscribed field and nothing else
        subscription = NewsletterSubscription.objects.filter(user=request.user).values("unsubscribed").first()
        
        if  subscription is None:
            subscribed = False
        else:
            is_subscribed =  subscription["unsubscribed"]
            subscribed    = not is_subscribed
       
    except Exception as e:
       print(f"Error fetching subscription model object: {e}")
      
    
    else:
        if subscribed:
            subscription_session = get_session(request, session_name="email") 
            if not subscription_session:
                set_session(request, "email")
                subscription_session = get_session(request, session_name="email") 
    
    return {
        "subscription_session": subscription_session
    }


