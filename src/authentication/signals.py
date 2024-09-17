from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import BanUser


    
@receiver(pre_delete, sender=BanUser)
def post_delete_un_ban_user(sender, instance, *args, **kwargs):
    """If the last ban related to a user is deleted, the user is automatically unbanned."""
  
    ban_record = BanUser.objects.filter(user=instance.user).first()

    if ban_record:
        ban_record.un_ban()


    

      