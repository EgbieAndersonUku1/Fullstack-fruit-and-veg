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

