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
        
    FREQUENCY_MAPPING = {
        "d": "Daily",
        "w": "Weekly",
        "bw": "Bi-weekly",
        "m": "Monthly",
        "q": "Quarterly",
    }
    
    class Frequency:
        DAILY     = "d"
        WEEKLY    = "w"
        BI_WEEKLY = "bw"
        MONTHLY   = "m"
        QUARTERLY = "q"
        CHOICES = [
            (DAILY, "Daily"), 
            (WEEKLY, "Weekly"), 
            (BI_WEEKLY, "Bi-weekly"), 
            (MONTHLY, "Monthly"), 
            (QUARTERLY, "Quarterly")
        ]
    
    title                    = models.CharField(max_length=255, default="General Newsletter") 
    user                     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="newsletter_subscriptions")
    email                    = models.EmailField(max_length=255, unique=True)
    subscribed_on            = models.DateTimeField(auto_now_add=True)
    modified_on              = models.DateTimeField(auto_now=True)
    unsubscribed             = models.BooleanField(default=False) 
    frequency                = models.CharField(choices=Frequency.CHOICES, max_length=2, default=Frequency.MONTHLY)
    unsubscribed_on          = models.DateTimeField(blank=True, null=True)
    reason_for_unsubscribing = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.title} - {self.email}"
     
    @property
    def date_unsubscribed(self):
        """
        Returns the date the user unsubscribed, to be used in the admin interface.
        
        If the user has unsubscribed, this will display the 'unsubscribed_on' date.
        If not, it will display 'N/A' to indicate no unsubscription has occurred.
        
        Returns:
            str: 'N/A' if the user has not unsubscribed, otherwise the date they unsubscribed.
        """
        return "N/A" if self.unsubscribed_on is None else self.unsubscribed_on

    @property
    def get_frequency(self):
        """
        Returns a human-readable frequency name.

        The database stores the frequency as single letters to save space.
        This method translates the stored frequency code into a descriptive 
        string format when accessed.

        Frequency mapping:
            'd'  -> "Daily"
            'w'  -> "Weekly"
            'bw' -> "Bi-weekly"
            'm'  -> "Monthly"
            'q'  -> "Quarterly"

        Example:
            If the frequency is stored as 'd', this method returns "Daily".
        """
        return self.FREQUENCY_MAPPING.get(self.frequency, "Unknown")
    
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
            self.unsubscribed      = True
            self.unsubscribed_on   = timezone.now()
            self.save()
    
    def subscribe(self):
        """
        Mark the user as subscribed.
        """
        if self.unsubscribed:
            self.subscribed_on = timezone.now()
            self.unsubscribed  = False
            self.save()

    def _is_user_instance_valid(user):
        if not isinstance(user, User):
            raise TypeError(f"Expected an instance of User, got {type(user).__name__}")
        

class NewsletterSubscriptionHistory(models.Model):
    title                    = models.CharField(max_length=255) 
    user                     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscription_history")
    email                    = models.EmailField(max_length=255)
    action                   = models.CharField(max_length=50)  # e.g., 'subscribed' or 'unsubscribed'
    timestamp                = models.DateTimeField(auto_now_add=True)
    unsubscribed_on          = models.DateTimeField(blank=True, null=True)
    frequency                = models.CharField(max_length=2, choices=NewsletterSubscription.Frequency.CHOICES, null=True, blank=True)
    reason_for_unsubscribing = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name         = "Subscription History"
        verbose_name_plural  = "Subscription Histories"
        
    def __str__(self) -> str:
        return f"{self.email} - {self.action} on {self.timestamp}"


class UnsubscribedNewsletterSubscription(NewsletterSubscription):
    class Meta:
        proxy              = True
        verbose_name        = "Unsubscribed Subscription"
        verbose_name_plural = "Unsubscribed Subscriptions"


class SubscribedNewsletterSubscription(NewsletterSubscription):
    class Meta:
        proxy               = True
        verbose_name        = "Subscribed Subscription"
        verbose_name_plural = "Subscribed Subscriptions"
        


class SubscriptionMessage:
    UNSUBSCRIBED = "Successfully unsubscribed the user."
    ERROR        = "Something went wrong, and the user couldn't be unsubscribed. Please try again later."
