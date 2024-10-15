from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone

from .models import Testimonial
from authentication.utils.send_emails_types import notify_user_of_approved_testimonial


@receiver(pre_save, sender=Testimonial)
def pre_save_testimonial(sender, instance, *args, **kwargs):
    """Before the testimonial is saved, check if it is approved and set the approval date."""
    
    if instance:
        
        # Only send it once
        if instance.is_approved and instance.date_approved is None:
            instance.date_approved = timezone.now() 
            
            try:
                notify_user_of_approved_testimonial(
                subject="Your testimonial has been approved",
                user=instance.author,
                )
                print(f"Notification sent to {instance.author} regarding the approval of their testimonial.")

            except Exception as e:
                # will add logger later but for now use
                print(f"Something went wrong with sending notification to user: {instance.author}. Error - {e}")
   