from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, UserProfile



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