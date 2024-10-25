from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from .models import NewsletterSubscription
from utils.send_emails_types import notify_admin_of_user_unsubscription


@receiver(pre_save, sender=NewsletterSubscription)
def pre_save_newsletter(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email = instance.email.lower()
        
        if instance.unsubscribed:
            if not instance.unsubscribed_on:
                instance.unsubscribed_on = timezone.now()
                
            subject = f"Unsubscribe Notification - {instance.user.username.title()}"
            notify_admin_of_user_unsubscription(subject, user=instance)
            


@receiver(post_save, sender=NewsletterSubscription)
def post_save_newsletter(sender, instance, created, *args, **kwargs):
    
    if created:
        if instance.unsubscribed:
            if not instance.unsubscribed_on:
                instance.unsubscribed_on = timezone.now()
                instance.save()
                
            subject = f"Unsubscribe Notification - {instance.user.username.title()}"
            notify_admin_of_user_unsubscription(subject, user=instance)