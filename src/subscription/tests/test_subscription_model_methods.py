from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from subscription.models import NewsletterSubscription
from .test_helper import create_test_user


class NewsletterSubscriptionMethodTest(TestCase):
    
    def setUp(self):
        self.title = "Test subscription title"
        self.email = "test_subscription@example.com"
        self.user  = create_test_user()
        self.newsletter_subscription = NewsletterSubscription.objects.create(
            title=self.title,
            user=self.user,
            email=self.email
        )
    
    def test_creation_count(self):
        """Test that exactly one subscription is created"""
        num_created = NewsletterSubscription.objects.count()
        self.assertEqual(num_created, 1)
        
    def test_date_unsubscribed_property_returns_correct_value_when_field_is_empty(self):
        """Test that prorpery returns the correct value when empty"""
        
        EXPECTED_VALUE = "N/A"
        self.newsletter_subscription.refresh_from_db()
        
        self.assertIsNone(self.newsletter_subscription.unsubscribed_on)
        self.assertEqual(self.newsletter_subscription.date_unsubscribed, EXPECTED_VALUE, 
                 "Expected 'date_unsubscribed' to return 'N/A' when 'unsubscribed_on' is None")

    def test_date_unsubscribed_property_returns_formatted_date_when_field_is_set(self):
        """Test that property returns formatted date when unsubscribed_on is not empty"""
        
        unsubscribe_date = timezone.now()
        self.newsletter_subscription.unsubscribed_on = timezone.now()
        self.newsletter_subscription.save()
        self.newsletter_subscription.refresh_from_db()
     
        expected_date = unsubscribe_date.strftime('%Y-%m-%d')
    
        # Assert that the property returns the correctly formatted date
        self.assertEqual(self.newsletter_subscription.date_unsubscribed, expected_date)

    def test_get_frequency_returns_readable_format(self):
        """Test if get_frequency method returns a readable format when called"""

        EXPECTED_FREQUENCY_NAMES = ["Daily", "Weekly", "Bi-weekly", "Monthly", "Quarterly"]
        frequencies = [
            NewsletterSubscription.Frequency.DAILY,
            NewsletterSubscription.Frequency.WEEKLY,
            NewsletterSubscription.Frequency.BI_WEEKLY,
            NewsletterSubscription.Frequency.MONTHLY,
            NewsletterSubscription.Frequency.QUARTERLY,
        ]
        
        for index, frequency in enumerate(frequencies):
            with self.subTest(frequency=frequency):
                self.newsletter_subscription.frequency = frequency
                self.newsletter_subscription.save()
                self.newsletter_subscription.refresh_from_db()
                
                # Ensure that get_frequency returns the expected readable format
                self.assertEqual(self.newsletter_subscription.get_frequency, EXPECTED_FREQUENCY_NAMES[index])
                
                # Check that get_frequency returns a string
                self.assertIsInstance(self.newsletter_subscription.get_frequency, str)
