from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from subscription.models import NewsletterSubscription
from .test_helper import create_test_user


class NewsletterSubscriptionTest(TestCase):
    
    def setUp(self):
        self.title = "Test subscription title"
        self.email = "test_subscription@example.com"
        self.user  = create_test_user()
        self.newsletter_subscription = NewsletterSubscription.objects.create(
            title=self.title,
            user=self.user,
            email=self.email,
            subscribed_on=timezone.now(),
        )
    
    def test_creation_count(self):
        """Test that exactly one subscription is created"""
        num_created = NewsletterSubscription.objects.count()
        self.assertEqual(num_created, 1)
    
    def test_title_field_matches_expected_value(self):
        """Test that the title field matches the expected title value"""
        self.newsletter_subscription.refresh_from_db()
        self.assertEqual(self.newsletter_subscription.title, self.title)
    
    def test_email_field_matches_expected_value(self):
        """Test that the email field matches the expected email value"""
        self.newsletter_subscription.refresh_from_db()
        self.assertEqual(self.newsletter_subscription.email, self.email)
        
    def test_user_field_matches_expected_user(self):
        """Test that the correct user is assigned to the user field"""
        self.newsletter_subscription.refresh_from_db()
        self.assertEqual(self.newsletter_subscription.user, self.user)
    
    def test_subscribed_on_date_field_is_not_empty_when_saved(self):
        """Test the subscribed on date field correctly assigns a given time upon creation"""
        self.newsletter_subscription.refresh_from_db()
        current_date_time = timezone.now()
        
        subscription_date = self.newsletter_subscription.subscribed_on
        self.assertIsNotNone(subscription_date)
        self.assertLessEqual(subscription_date, current_date_time)
    
    def test_user_is_automatically_subscribed_on_creation(self):
        """Test that the unsubscribed field is false meaning that the user is automatically subscribed when created"""
        self.newsletter_subscription.refresh_from_db()
        self.assertFalse(self.newsletter_subscription.unsubscribed)
    
    def test_unsubscribed_date_field_is_empty_on_creation(self):
        """Test that the unsubscribed field date is empty when created"""
        self.newsletter_subscription.refresh_from_db()
        self.assertIsNone(self.newsletter_subscription.unsubscribed_on)
        
    def test_unsubscribed_date_field_can_be_set(self):
        """Test that the unsubscribed field date is empty when created"""
        self.newsletter_subscription.refresh_from_db()
        self.assertIsNone(self.newsletter_subscription.unsubscribed_on)
        
        self.newsletter_subscription.unsubscribed_on = timezone.now()
        self.newsletter_subscription.save()
        
        self.newsletter_subscription.refresh_from_db()
        self.assertIsNotNone(self.newsletter_subscription.unsubscribed_on)
        
        current_date_time_now = timezone.now()
        
        # check if the datetime is less than new created time
        self.assertLessEqual(self.newsletter_subscription.unsubscribed_on, current_date_time_now)
        
    def test_if_default_title_is_set_upon_creation(self):
        """Test if the default title is set upon creation"""

        EXPECTED_DEFAULT_TITLE       = "General Newsletter"
        self.email                   = "test2_subscription@example.com"
        self.user                    = create_test_user(username="test1", email="test2@example.com")
        
        self.newsletter_subscription = NewsletterSubscription.objects.create(
            user=self.user,
            email=self.email
        )
        self.assertEqual(self.newsletter_subscription.title, EXPECTED_DEFAULT_TITLE)
        
    def test_reason_for_unsubscribing_field_is_blank_upon_creation(self):
        """Test that field reason for unsubscribing is created as a blank field when created"""
        self.newsletter_subscription.refresh_from_db()
        self.assertIsNone(self.newsletter_subscription.reason_for_unsubscribing)
    
    def test_reason_for_unsubscribing_field_can_be_set(self):
        """Test if the reason for unsubscribing field can be set"""
        
        # test if the field is none first
        self.newsletter_subscription.refresh_from_db()
        
        self.assertIsNone(self.newsletter_subscription.reason_for_unsubscribing)
        
        REASON_FOR_UNSUBSCRIBING = "Test unsubscribing reason here"
        self.newsletter_subscription.reason_for_unsubscribing = REASON_FOR_UNSUBSCRIBING
        self.newsletter_subscription.save()
        
        self.newsletter_subscription.refresh_from_db()
        self.assertIsNotNone(self.newsletter_subscription.reason_for_unsubscribing)
        self.assertEqual(self.newsletter_subscription.reason_for_unsubscribing, REASON_FOR_UNSUBSCRIBING)    
    
    def test_frequency_defaults_to_monthly(self):
        """Test that frequency field has a default setting of monthly"""
        self.newsletter_subscription.refresh_from_db()
        self.assertEqual(self.newsletter_subscription.frequency, NewsletterSubscription.Frequency.MONTHLY)
    
    def test_frequency_can_be_updated_to_all_possible_values(self):
        """Test that the frequency field can be updated to each possible value"""
     
        frequencies = [
            NewsletterSubscription.Frequency.DAILY,
            NewsletterSubscription.Frequency.WEEKLY,
            NewsletterSubscription.Frequency.BI_WEEKLY,
            NewsletterSubscription.Frequency.MONTHLY,
            NewsletterSubscription.Frequency.QUARTERLY,
        ]

        for frequency in frequencies:
            with self.subTest(frequency=frequency):
                self.newsletter_subscription.frequency = frequency
                self.newsletter_subscription.save()
                self.newsletter_subscription.refresh_from_db()
                self.assertEqual(self.newsletter_subscription.frequency, frequency)

    def test_title_field_length_does_not_exceed_maximum_length(self):
        """Test that title field does not exceed the expected length limit"""
        
        long_title  = "t" * 355  # max_length=255 on the db

        self.newsletter_subscription.title = long_title

        # Attempt to save and expect a ValidationError due to length
        with self.assertRaises(ValidationError):
            self.newsletter_subscription.full_clean()  # this will triggers the model field validation
            self.newsletter_subscription.save()
    
    def test_email_field_length_does_not_exceed_maximum_length(self):
        """Test that email field does not exceed the expected length limit"""
        
        long_email  = "t" * 355  # max_length=255 on the db
        long_email  =  f"{long_email}@example.com"
        self.newsletter_subscription.email = long_email

        # Attempt to save and expect a ValidationError due to length
        with self.assertRaises(ValidationError):
            self.newsletter_subscription.full_clean()  # this will triggers the model field validation
            self.newsletter_subscription.save()
            
    def test_subscription_deleted_when_user_is_deleted(self):
        """Test that deleting a user also deletes their newsletter subscriptions"""
        
        # Verify the subscription exists initially
        self.assertEqual(NewsletterSubscription.objects.count(), 1)
        
        self.user.delete()
        
        # Check that the subscription was deleted as well
        self.assertEqual(NewsletterSubscription.objects.count(), 0)
    
   

        
        


        
        