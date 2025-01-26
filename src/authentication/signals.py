from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from dotenv import load_dotenv
from os import getenv

from .models import BanUser, UserBaseLineData
from utils.utils import hash_ip

    
@receiver(pre_delete, sender=BanUser)
def post_delete_un_ban_user(sender, instance, *args, **kwargs):
    """If the last ban related to a user is deleted, the user is automatically unbanned."""
  
    ban_record = BanUser.objects.filter(user=instance.user).first()

    if ban_record:
        ban_record.un_ban()


    
@receiver(pre_save, sender=UserBaseLineData)
def pre_save_user_base_line_data(sender, instance,  *args, **kwargs):
    
    if instance:
        # ensure that ip is always saved as a hash
        if not instance.client_ip_address.startswith("hash"):
            instance.client_ip_address = hash_ip(ip_address=instance.client_ip_address, secret_key=getenv("SECRET_KEY"))