from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from utils.tasks import notify_admin_of_user_unsubscription, notify_admin_of_new_subscriber
from .models import NewsletterSubscription, NewsletterSubscriptionHistory


@receiver(pre_save, sender=NewsletterSubscription)
def pre_save_newsletter(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email = instance.email.lower()
        
