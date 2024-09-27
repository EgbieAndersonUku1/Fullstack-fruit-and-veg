from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth import get_user_model

from utils.generator import generate_token
from utils.country_parser import parse_country_file


COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")



# Create your models here.
User = get_user_model()

class BaseAddress(models.Model):
    country            = models.CharField(max_length=40, choices=COUNTRIES_CHOICES, default=COUNTRIES_CHOICES[0])
    address_1          = models.CharField(verbose_name="Address One", max_length=200, blank=False, null=False)
    address_2          = models.CharField(verbose_name="Address Two (Optional)", max_length=200, blank=True, null=True)
    city               = models.CharField(max_length=50, blank=False, null=False)
    state              = models.CharField(max_length=50, blank=False, null=False)
    postcode           = models.CharField(max_length=10, blank=False, null=False)
    modified           = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    date_created       = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)

    class Meta:
        abstract = True



   
class UserProfile(models.Model):
    PROFILE_PIC_PATH   = "users/profile/pic/"
    COVER_PHOTO_PATH   = "users/cover/photo/"
    
    first_name         = models.CharField(max_length=40, blank=False, null=False)
    last_name          = models.CharField(max_length=40, blank=False, null=False)
    telephone          = models.CharField(max_length=12, null=True, blank=True)
    mobile             = models.CharField(max_length=12, blank=False, null=False)
    profile_pic        = models.ImageField(verbose_name="Profile picture", null=True, blank=True, upload_to=PROFILE_PIC_PATH)
    cover_photo        = models.ImageField(verbose_name="Cover picture", null=True, blank=True, upload_to=COVER_PHOTO_PATH)
    user               = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", editable=False)
    date_created       = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)

    
    def num_of_shipping_addresses(self):
        return self.shipping_addresses.count()
       
    def num_of_billing_addresses(self):
        return self.billing_addresses.count()
      
    @property
    def full_name(self):
        """
        Returns the user's full name in title case, combining 
        first_name and last_name. If either first_name or last_name 
        is missing, returns an empty string.
        
        :return: str - The formatted full name of the user.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name.title()} {self.last_name.title()}"
        return ""  

    @property
    def username(self):
        """
        Returns the username in title case. This method is particularly 
        useful for displaying the username in the UserProfile admin page, 
        providing a more readable format in the admin interface.
        
        :return: str - The formatted username of the user.
        """
        return self.user.username.title()
    
    def __str__(self):
        return f"Profile for {self.user.username}"

    def num_of_gift_cards(self):
        return self.gift_cards.count()


     
class GiftCard(models.Model):
    card_type        = models.CharField(max_length=100, blank=True, null=True)
    code             = models.CharField(max_length=43, unique=True, blank=True, null=True)
    is_active        = models.BooleanField(default=False)
    expiration_date  = models.DateField(null=True, blank=True)
    does_not_expire  = models.BooleanField(default=False)
    user_profile     = models.ForeignKey(UserProfile, related_name="gift_cards", on_delete=models.CASCADE, null=True, blank=True)    
    value            = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_redeemed      = models.BooleanField(default=False)
    date_created     = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name        = "gift card"
        verbose_name_plural = "gift cards"
        
    def __str__(self):
        user = self.user_profile.user if self.user_profile else None
        return f"Gift card for {user.username.title() if user else 'No User'} with the amount of £{self.value:.2f}"
 
    def is_valid(self, code):
        """Check if the gift card is still valid, considering does_not_expire."""
        
        if self.code != code:
            return False
        
        current_date    = timezone.now().date()
        expiration_date = datetime.strptime(str(self.expiration_date), "%Y-%m-%d").date()
        
        is_active_and_not_redeemed = self.is_active and not self.is_redeemed
        is_not_expired             = (self.does_not_expire or self.expiration_date is None) or (expiration_date >= current_date)
        return is_active_and_not_redeemed and is_not_expired

    def apply(self, amount, save=True):
        """Apply an amount to the gift card and reduce its value."""
        
        if self.value == 0:
            self.is_redeemed = True
            self.is_active   = False
        if not self.is_active:
            raise ValueError("The gift card is not valid")
        if not isinstance(amount, Decimal):
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
    
    def activate(self, save=True):
        """Activate the gift card."""
        self.is_active = True
        if save:
            self.save()
    
    @classmethod
    def issue_gift_card(cls, card_type=None, amount=None, expiry_date=None, user=None, does_not_expire=False, is_active=True):
        """Class method to issue a new gift card."""
        
        gift_card      = cls()
        gift_card.code = generate_token()
        
        if user:
            gift_card.user_profile = user
        
        gift_card.activate(save=False) if is_active else gift_card.deactivate(save=False)
        gift_card.set_card_type(card_type)
        gift_card.set_expiry_date(expiry_date, does_not_expire)
        gift_card.set_amount(amount)
        gift_card.save()
        
        return gift_card
        
    def set_expiry_date(self, expiry_date=None, does_not_expire=False, save=True):
        """Helper method to set the expiration date."""
        
        if does_not_expire:
            self.does_not_expire = True
        elif expiry_date and not does_not_expire:
            if isinstance(expiry_date, str):
                # If expiry_date is a string, parse it into a date object
                try:
                    self.expiration_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            elif isinstance(expiry_date, date):
                self.expiration_date = expiry_date
            self.does_not_expire = False
        
        if save:
            self.save()
    
    def set_amount(self, amount=None):
        """Set the amount for the gift card"""
        
        if not isinstance(amount,  Decimal):
            raise TypeError("The amount must be either an integer or a float")
        if not amount:
            raise ValueError("An amount must be entered")
        if amount <= 0:
            raise ValueError("The amount must be greater than zero.")

        self.value = amount
        
    def set_card_type(self, card_type=None):
        """Takes a card type e.g reward card, promotion card and sets it to the gift card"""
        if card_type:
            self.card_type = card_type
        
      

class BillingAddress(BaseAddress):
    user_profile    = models.ForeignKey(UserProfile, related_name="billing_addresses", on_delete=models.CASCADE, blank=True, null=False)
    primary_address = models.BooleanField(default=False)

    class Meta:
        verbose_name        = "Billing Address"
        verbose_name_plural = "Billing Addresses"
    
    def mark_as_primary(self, save=True):
        """
        Set this billing address as the primary address for the user profile.
        """
        self.primary_address = True
        if save:
            self.save()
    
    def unmark_as_primary(self, save=True):
        """
        Set this billing address as not the primary address for the user profile.
        """
        self.primary_address = False
        if save:
            self.save()

    @classmethod
    def get_primary_address(cls, user):
        """
        Takes a user model and returns the primary address belong to that user
        
        :Params
            - User (model): The user model belong to the user
        
        :Returns
            - Returns the shipping address or none 
            
        Example Usage:
           >>> user = User.get_by_email(email="some_email@example")
           >>> primary_address = UserProfile.get_primary_address(user=user)
           >>> 
        """
        return cls.objects.filter(user_profile=user.profile, primary_address=True).first()
    
    
class ShippingAddress(BaseAddress):
    user_profile       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="shipping_addresses",  blank=True, null=True)

    class Meta:
        verbose_name        = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

