from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import NewsletterSubscription


@receiver(pre_save, sender=NewsletterSubscription)
def pre_save_newsletter(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email = instance.email.lower()