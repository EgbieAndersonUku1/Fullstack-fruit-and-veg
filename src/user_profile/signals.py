from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import User, UserProfile, BillingAddress



@receiver(post_save, sender=User)
def create_user_profile_receiver(sender, instance, created, *args, **kwargs):
    
    if created:
        UserProfile.objects.create(user=instance)
    else:
        handle_existing_user_profile(instance)
    

def handle_existing_user_profile(user):
    
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user)
    else:
        profile.save()
        

@receiver(post_save, sender=BillingAddress)
def handle_billing_address_update(sender, instance, **kwargs):
    
    if instance.primary_address:
        # Unmark all other primary addresses for this user profile except for one excluded
        BillingAddress.objects.filter(user_profile=instance.user_profile, primary_address=True).exclude(pk=instance.pk).update(primary_address=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
  
  
    


@receiver(pre_save, sender=BillingAddress)
def handle_billing_address_update(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance already exists (i.e., it's an update, not a creation)
        # Get the current instance from the database
        try:
            current_instance = BillingAddress.objects.get(pk=instance.pk)
        except BillingAddress.DoesNotExist:
            current_instance = None

        # If the address is being updated to be primary, unmark other primary addresses
        if instance.primary_address and current_instance and current_instance.primary_address != instance.primary_address:
            # Unmark all other primary addresses for this user profile
            BillingAddress.objects.filter(user_profile=instance.user_profile, primary_address=True).exclude(pk=instance.pk).update(primary_address=False)

    elif instance.primary_address:
        # If this is a new instance and it's marked as primary, unmark all other primary addresses for this user profile
        BillingAddress.objects.filter(user_profile=instance.user_profile, primary_address=True).update(primary_address=False)