from datetime import timedelta
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
            email=self.email,
        )
    
    def test_creation_count(self):
        """Test that exactly one subscription is created"""
        num_created = NewsletterSubscription.objects.count()
        self.assertEqual(num_created, 1)
        
    def test_created_at_field_is_set_on_upon_creation(self):
        """Test if the created_at field is correctly set when a new subscription is created."""
        
        new_user = create_test_user(username="new_user", email="new_user@example.com")
        
        new_subscription = NewsletterSubscription.objects.create(
            title="Newsletter Title",
            user=new_user,
            email=new_user.email,
        )
        
        new_subscription.refresh_from_db()
        
        created_at = new_subscription.created_at
        
        self.assertIsNotNone(created_at, "Expected 'created_at' to be set upon creation.")
        
        # Assert that created_at is within a reasonable time range (e.g., the creation time should be within 1 second of now)
        self.assertAlmostEqual(
            created_at, timezone.now(), delta=timedelta(seconds=1),
            msg=f"Expected 'created_at' to be close to the current time, but got {created_at}."
        )
    
    def test_unsubscribed_on_is_is_none_upon_creation(self):
        """Test that unsubscribed date field is none upon creation"""
        
        self.newsletter_subscription.refresh_from_db()
        self.assertIsNone(self.newsletter_subscription.subscribed_on)
     
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
                
    def test_get_by_user_method_returns_subscription_model(self):
        """
        Test that get_by_user method returns the subscription model via the user model, 
        including unsubscribed records.
        """
        
        # Check that the method returns a subscription model when a user is subscribed
        subscribed_subscription = NewsletterSubscription.get_by_user(user=self.user)
        self.assertIsNotNone(subscribed_subscription, "Expected subscription to be returned for a subscribed user.")
        self.assertFalse(subscribed_subscription.unsubscribed, "Expected 'unsubscribed' to be False initially.")

        # Test that method returns None when a user isn't subscribed
        not_subscribed_user       = create_test_user(username="unsubscribed_user", email="unsubscribed_user@example.com")
        unsubscribed_subscription = NewsletterSubscription.get_by_user(user=not_subscribed_user)
        self.assertIsNone(unsubscribed_subscription, "Expected None for a user with no subscription.")
        
        # Test that we can retrieve the user's subscription model even if they are unsubscribed
        # Set the subscription to unsubscribed and check that it still appears in get_by_user
        subscribed_subscription.unsubscribed = True
        subscribed_subscription.save()
        subscribed_subscription.refresh_from_db()
        
        # Fetch the subscription again to confirm it includes the unsubscribed state
        unsubscribed_subscription_after_update = NewsletterSubscription.get_by_user(user=self.user)
        self.assertIsNotNone(unsubscribed_subscription_after_update, "Expected subscription to be returned even if unsubscribed.")
        self.assertTrue(unsubscribed_subscription_after_update.unsubscribed, "Expected 'unsubscribed' to be True after update.")

    def test_get_by_email_and_user_returns_subscription_model(self):
        """
        Test that get_by_user_and_email returns a subscription model only when 
        provided with a valid user and matching email.
        """
        
        subscribed_email = self.user.email
        
        # Test with correct subscribed email
        subscription = NewsletterSubscription.get_by_user_and_email(user=self.user, email=subscribed_email)
        self.assertIsNotNone(subscription, "Expected a subscription to be returned for a valid user and email.")
        
        # Test with a nonexistent user and email
        nonexistent_user = create_test_user(username="nonexistent_user", email="nonexistent_user@example.com")
        nonexistent_email = nonexistent_user.email 
        
        subscription = NewsletterSubscription.get_by_user_and_email(user=nonexistent_user, email=nonexistent_email)
        self.assertIsNone(subscription, "Expected None since both the user and email are invalid.")
        
        # Test with valid user but invalid email
        subscription = NewsletterSubscription.get_by_user_and_email(user=self.user, email=nonexistent_email)
        self.assertIsNone(subscription, "Expected None since the user is valid but the email does not match.")
        
        # Test with invalid user but valid email
        subscription = NewsletterSubscription.get_by_user_and_email(user=nonexistent_user, email=subscribed_email)
        self.assertIsNone(subscription, "Expected None since the email is valid but the user is invalid.")

    def test_get_by_email_and_user_raises_type_error_if_not_user_instance(self):
        """Test that get_by_email_and_user raises TypeError if the instance passed is not a User instance."""
        
        expected_message = "Expected an instance of User, got NewsletterSubscription"
        
        with self.assertRaisesRegex(TypeError, expected_message):
            
            # Pass a NewsletterSubscription instance instead of a User instance to trigger the TypeError
            NewsletterSubscription.get_by_user_and_email(user=self.newsletter_subscription, email=self.user.email)

    def test_get_by_user_raises_type_error_if_not_user_instance(self):
        """Test that get_by_email_and_user raises TypeError if the instance passed is not a User instance."""
        
        expected_message = "Expected an instance of User, got NewsletterSubscription"
        
        with self.assertRaisesRegex(TypeError, expected_message):
            # Pass a NewsletterSubscription instance instead of a User instance to trigger the TypeError
            NewsletterSubscription.get_by_user_and_email(user=self.newsletter_subscription, email=self.user.email)
    
    def test__str__method_returns_correct_string(self):
        """Test if that the correct string for the user model is returned"""
        expected_string = f"{self.newsletter_subscription.title} - {self.newsletter_subscription.email}"
        self.assertEqual(str(self.newsletter_subscription), expected_string)
    
    def test_subscribe_method_correctly_subscribes_user(self):
        """Test if the subscribe method correctly subscribes an unsubscribed user and updates relevant fields."""
        
        new_user = create_test_user(username="new_user", email="new_user@example.com")
        
        # Create a subscription with an unsubscribed user
        unsubscribed_user = NewsletterSubscription.objects.create(
            title=self.title,
            user=new_user,
            email=new_user.email,
            unsubscribed=True,  # Explicitly set to unsubscribed
        )
        
        # Assert initial state: user is unsubscribed, and subscribed_on is None
        self.assertTrue(unsubscribed_user.unsubscribed)
        self.assertIsNone(unsubscribed_user.subscribed_on, "Expected 'subscribed_on' to be None initially")

        unsubscribed_user.subscribe()
        unsubscribed_user.refresh_from_db()

        # # Assert that the user is now subscribed
        self.assertFalse(unsubscribed_user.unsubscribed)

        # # Assert that subscribed_on is now set to the current time (or close to it)
        self.assertIsNotNone(unsubscribed_user.subscribed_on, "Expected 'subscribed_on' to be set after subscribing")
        self.assertAlmostEqual(unsubscribed_user.subscribed_on, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_subscribe_method_correctly_unsubscribes_user(self):
        """Test if the unsubscribe method correctly unsubscribes a user and updates relevant fields."""
        
        new_user = create_test_user(username="new_user", email="new_user@example.com")
        
        # Create a subscription with an subscribed user
        subscribed_user = NewsletterSubscription.objects.create(
            title=self.title,
            user=new_user,
            email=new_user.email,
            subscribed_on=timezone.now(),
        )
        
        subscribed_date = subscribed_user.subscribed_on
        
        # Assert initial state: user is subscribed, subscribed_on is not None and unsubscribed_on is None
        self.assertFalse(subscribed_user.unsubscribed)
        self.assertIsNotNone(subscribed_user.subscribed_on, "Expected 'subscribed_on' to have date set and not be None initially")
        self.assertIsNotNone(subscribed_date, "Expected 'subscribed_on' to be set after subscribing")
            
        subscribed_user.unsubscribe()
        subscribed_user.refresh_from_db()
        
        # Assert that the user is now unsubscribed
        self.assertTrue(subscribed_user.unsubscribed)
        
        # Assert that unsubscribed_on is now set to the current time and is later than subscribed_on
        self.assertIsNotNone(subscribed_user.unsubscribed_on, "Expected 'unsubscribed_on' to be set after unsubscribing")
        self.assertGreaterEqual(subscribed_user.unsubscribed_on, subscribed_date)
        
        # Check that unsubscribed_on is close to now
        self.assertAlmostEqual(subscribed_user.unsubscribed_on, timezone.now(), delta=timedelta(seconds=1))

    def tearDown(self):
        """Clean up test data after each test method is executed."""
        NewsletterSubscription.objects.all().delete()
        self.user.delete()
