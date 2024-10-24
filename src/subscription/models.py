from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

User = get_user_model()


class NewsletterSubscription(models.Model):
    class Meta:
        verbose_name        = "All Newsletter Subscription"
        verbose_name_plural = "All Newsletter Subscriptions"
        indexes = [
            models.Index(fields=['user'])  # Index user only, email is already unique
        ]
        
    class Frequency:
        DAILY     = "d"
        WEEKLY    = "w"
        BI_WEEKLY = "BW"
        MONTHLY   = "m"
        QUARTERLY = "q"
        CHOICES = [
            (DAILY, "Daily"), 
            (WEEKLY, "Weekly"), 
            (BI_WEEKLY, "Bi-weekly"), 
            (MONTHLY, "Monthly"), 
            (QUARTERLY, "Quarterly")
        ]
        
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="newsletter_subscriptions")
    email          = models.EmailField(max_length=255, unique=True)
    subscribed_on  = models.DateTimeField(auto_now_add=True)
    modified_on    = models.DateTimeField(auto_now=True)
    unsubscribed   = models.BooleanField(default=False) 
    frequency      = models.CharField(choices=Frequency.CHOICES, max_length=2, default=Frequency.MONTHLY)
    
    def __str__(self) -> str:
        return self.email 
    
    @classmethod
    def get_by_user(cls, user: "User"): 
        """
        Takes a user instance and returns the subscription associated with that user.
        Returns None if no subscription is associated with the account.

        Raises:
            TypeError: If the provided user is not an instance of the User model.

        Args:
            user (User): The user instance used to retrieve the subscription.

        Returns:
            NewsletterSubscription: The subscription instance associated with the user.
            None: If no subscription is found for the user.
        """
        cls._is_user_instance_valid(user)
        
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_by_user_and_email(cls, user: "User", email:str): 
        """
        Takes a user instance and email and returns the subscription associated with that user.
        Returns None if no subscription is associated with the account.

        Raises:
            TypeError: If the provided user is not an instance of the User model.

        Args:
            user (User): The user instance used to retrieve the subscription.
            email (Str): The email used to retreive the subscription

        Returns:
            NewsletterSubscription: The subscription instance associated with the user.
            None: If no subscription is found for the user.
        """

        cls._is_user_instance_valid(user)
        return cls.objects.filter(user=user, email=email.lower()).first()
    
    def unsubscribe(self):
        """
        Mark the user as unsubscribed.
        """
        if not self.unsubscribed:
            self.unsubscribed = True
            self.save()
    
    def subscribe(self):
        """
        Mark the user as subscribed.
        """
        if self.unsubscribed:
            self.subscribed_on = timezone.now()
            self.unsubscribed  = False
            self.save()

    def _is_user_instance_valid(cls, user):
        if not isinstance(user, User):
            raise TypeError(f"Expected an instance of User, got {type(user).__name__}")
        
        
class UnsubscribedNewsletterSubscription(NewsletterSubscription):
    class Meta:
        proxy              = True
        verbose_name        = "Unsubscribed Newsletter Subscription"
        verbose_name_plural = "Unsubscribed Newsletter Subscriptions"



class SubscribedNewsletterSubscription(NewsletterSubscription):
    class Meta:
        proxy               = True
        verbose_name        = "Subscribed Newsletter Subscription"
        verbose_name_plural = "Subscribed Newsletter Subscriptions"