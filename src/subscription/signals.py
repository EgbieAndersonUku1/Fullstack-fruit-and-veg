from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from utils.send_emails_types import notify_admin_of_user_unsubscription, notify_admin_of_new_subscriber
from .models import NewsletterSubscription, NewsletterSubscriptionHistory


@receiver(pre_save, sender=NewsletterSubscription)
def pre_save_newsletter(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email = instance.email.lower()
        


@receiver(post_save, sender=NewsletterSubscription)
def post_save_newsletter(sender, instance, *args, **kwargs):
    
    if instance:
        if instance.unsubscribed:
            NewsletterSubscriptionHistory.objects.create(title="User has unsubscribed",
                                                         user=instance.user,
                                                         email=instance.email,
                                                         action="unsubscribed",
                                                         unsubscribed_on=timezone.now(),
                                                         start_date=instance.subscribed_on,
                                                         frequency=instance.frequency,
                                                         )
            
            # notify admin that user has unsubscribed
            subject = "Alert a user has unsubscribed"
            notify_admin_of_user_unsubscription(subject, user=instance)
        
        elif not instance.unsubscribed:
            NewsletterSubscriptionHistory.objects.create(title="User has re-subscribed",
                                                         user=instance.user,
                                                         email=instance.email,
                                                         action="re-subscribed",
                                                         unsubscribed_on=timezone.now(),
                                                         start_date=instance.subscribed_on,
                                                         frequency=instance.frequency,
                                                         )
            
            # notify admin that user has unsubscribed
            subject = "Subject: Subscriber Alert! 🎉"
            notify_admin_of_new_subscriber(subject, user=instance)
        
