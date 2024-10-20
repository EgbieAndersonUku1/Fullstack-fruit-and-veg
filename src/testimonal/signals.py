from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone

from .models import Testimonial
from authentication.utils.send_emails_types import notify_user_of_approved_testimonial, notify_user_of_admin_response


@receiver(pre_save, sender=Testimonial)
def pre_save_testimonial(sender, instance, *args, **kwargs):
    """Before the testimonial is saved, check if it is approved and set the approval date."""
    
    if instance:
        
        if not instance.pk or instance.pk:
           _convert_instance_fields_to_lowercase(instance)
        
        if instance.is_approved and instance.date_approved is None:
            instance.date_approved = timezone.now() 
            subject = "Your testimonial has been approved"
            _send_notification_to_user(notify_user_of_approved_testimonial, instance, subject)
        
        # Check if there's an admin response and send notification
        if instance.admin_response and not instance.has_admin_responded:
            subject = "You have received a response from the admin"
            instance.has_admin_responded = True
            _send_notification_to_user(notify_user_of_admin_response, instance, subject)
          

def _send_notification_to_user(send_email_func, instance, subject):
    """
    Helper function to send email notifications to users with error handling.
    """
    try:
        send_email_func(
            subject=subject,
            user=instance.author,
        )
        print(f"Notification sent to {instance.author} regarding the approval of their testimonial.")

    except Exception as e:
        # will add logger later but for now use
        print(f"Something went wrong with sending notification to user: {instance.author}. Error - {e}")


def _convert_instance_fields_to_lowercase(instance: Testimonial) -> None:
    """
    Converts specific fields of a Testimonial instance to lowercase.

    :param instance: 
        A Testimonial instance containing the fields to be modified.
    
    :returns:
        Returns None: The instance with title, company_name, country, and location fields are modified in place.
    """
    instance.title         = instance.title.lower()
    instance.company_name  = instance.company_name.lower()
    instance.country       = instance.country.lower()
    instance.location      = instance.location.lower()
  


