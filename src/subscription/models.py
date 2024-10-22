from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

User = get_user_model()


class NewsletterSubscription(models.Model):
    class Frequency:
        DAILY     = "d"
        WEEKLY    = "w"
        BI_WEEKLY = "BW"
        MONTHLY   = "m"
        QUARTELY  = "q"
        CHOICES = [(DAILY, "Daily"), (WEEKLY, "Weekly"), (BI_WEEKLY, "Bi-weekly"), (MONTHLY, "Montly"), (QUARTELY, "Quartely")]
        
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="newsletter_subscription")
    subscribed_on  = models.DateTimeField(auto_now_add=True)
    modified_on    = models.DateTimeField(auto_now=True)
    unsubscribed   = models.BooleanField(default=False) 
    frequency      = models.CharField(choices=Frequency.CHOICES, max_length=2, default=Frequency.MONTHLY)
    
    def __str__(self) -> str:
        return self.user.email 
    
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
            Subscription: The subscription instance associated with the user.
            None: If no subscription is found for the user.
        """

        if not isinstance(user, User):
            raise TypeError(f"Expected an instance of User, got {type(user).__name__}")

        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None
    
    def unsubscribe(self):
        """
        Mark the user as unsubscribed.
        """
        if self.unsubscribed:
            self.unsubscribed = True
            self.save()
    
    def subscribe(self):
        """
        Mark the user as subscribed
        """
        if not self.unsubscribe:
            self.subscribed_on = timezone.now()
            self.unsubscribe   = False
            self.save()
    
            