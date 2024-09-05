from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

from utils.generator import generate_token
from utils.country_parser import parse_country_file


COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")



# Create your models here.
User = get_user_model()


class BaseAddress(models.Model):
    country      = models.CharField(max_length=40, choices=COUNTRIES_CHOICES, default=COUNTRIES_CHOICES[0])
    address_1    = models.CharField(max_length=200, blank=True, null=True)
    address_2    = models.CharField(max_length=200, blank=True, null=True)
    city         = models.CharField(max_length=50, blank=True, null=True)
    postcode     = models.CharField(max_length=10, blank=True, null=True)
    modified     = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} for {self.user.username}"


class ShippingAddress(BaseAddress):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shipping_address")

    class Meta:
        verbose_name        = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"


class BillingAddress(BaseAddress):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name="billing_address")
    primary_address = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Billing Address"
        verbose_name_plural = "Billing Addresses"
        
        
class GiftCard(models.Model):
    name             = models.CharField(max_length=100, blank=True, null=True)
    code             = models.CharField(max_length=20, unique=True, default=generate_token)
    is_active        = models.BooleanField(default=True)
    expiration_date  = models.DateField(null=True, blank=True)
    user             = models.ForeignKey(User, related_name="gift_cards", on_delete=models.CASCADE, null=True, blank=True)
    value            = models.DecimalField(max_digits=10, decimal_places=2)
    date_created     = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Gift card for {self.user.username.title()} with the amount of £{self.value:.2f}"

    def is_valid(self, code):
        """Check if the gift card is still valid."""
        
        if self.code != code:
            return False
        
        current_date = timezone.now().date()
        return self.is_active and (self.expiration_date is None or self.expiration_date >= current_date)

    def apply(self, amount, save=True):
        """Apply an amount to the gift card and reduce its value."""
        
        if not self.is_active:
            raise ValueError("The gift card is not valid")
        if not isinstance(amount, (float, int)):
            raise TypeError("The amount must be an integer or a float.")
        if amount <= 0:
            raise ValueError("The amount must be greater than zero.")
        if amount > self.value:
            raise ValueError("Insufficient balance on the gift card.")
        
        self.value -= amount
        if save:
            self.save()

    def deactivate(self, save=True):
        """Deactivate the gift card."""
        self.is_active = False
        if save:
            self.save()


class UserProfile(models.Model):
    PROFILE_PIC_PATH   = "users/profile/pic/"
    COVER_PHOTO_PATH   = "users/cover/photo/"
    
    first_name         = models.CharField(max_length=40, null=True, blank=True)
    last_name          = models.CharField(max_length=40, null=True, blank=True)
    telephone          = models.CharField(max_length=12, null=True, blank=True)
    mobile             = models.CharField(max_length=12, null=True, blank=True)
    profile_pic        = models.ImageField(verbose_name="Profile picture", upload_to=PROFILE_PIC_PATH)
    cover_photo        = models.ImageField(verbose_name="Cover picture", null=True, blank=True, upload_to=COVER_PHOTO_PATH)
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    gift_cards         = models.ManyToManyField(GiftCard, related_name="profiles", blank=True)
    shipping_addresses = models.ManyToManyField(ShippingAddress, related_name="profiles", blank=True)
    billing_addresses  = models.ManyToManyField(BillingAddress, related_name="profiles", blank=True)
    date_created       = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

