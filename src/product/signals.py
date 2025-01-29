from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.forms import ValidationError


from utils.generator import generate_token
from .models import Product



@receiver(pre_save, sender=Product)
def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.sku:
        instance.sku = generate_token()
    if not instance.upc:
        instance.upc = generate_token()
        
    if len(instance.short_description) > 255:
        raise ValidationError("Short description cannot exceed 255 characters.")