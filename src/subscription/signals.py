from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import transaction
from .models import NewsletterSubscription, NewsletterSubscriptionHistory


@receiver(pre_save, sender=NewsletterSubscription)
def pre_save_newsletter(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email = instance.email.lower()
        


