from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction, IntegrityError


from subscription.models import NewsletterSubscription
from .test_helper import create_test_user


User = get_user_model()

class NewsletterSubscriptionIntegrationTest(TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_if_subscription_model_is_deleted_when_user_cascade_delete_is_used(self):
        """
        Test if the subscription model is deleted when the User model is deleted.
        """
        new_user = create_test_user()
        self.assertIsNotNone(new_user)

        # Create a subscription associated with the new user
        subscription = NewsletterSubscription.objects.create(
            title="Test subscription title",
            user=new_user,
            email="subscription_email@example.com",
            subscribed_on=timezone.now(),
            unsubscribed=False,
        )

        # Verify that the subscription exists
        self.assertTrue(NewsletterSubscription.objects.filter(pk=subscription.pk).exists())

        new_user.delete()

        # Verify that the subscription is deleted (cascade)
        self.assertFalse(NewsletterSubscription.objects.filter(pk=subscription.pk).exists())


    def test_deleting_a_subscription_does_not_delete_the_user_associated_within(self):
        """Test that deleting a subscription does not delete the associated user"""
        
        new_user = create_test_user()
        self.assertIsNotNone(new_user)
        
        subscription = NewsletterSubscription.objects.create(
            title="Test subscription title",
            user=new_user,
            email="subscription_email@example.com",
            subscribed_on=timezone.now(),
            unsubscribed=False,
        )

        # test that subscription model has been created
        self.assertIsNotNone(NewsletterSubscription.objects.filter(pk=subscription.pk).exists())
        
        # delete the subscription model
        subscription.refresh_from_db()
        subscription.delete()
        
        # check if the subscription is deleted
        self.assertFalse(NewsletterSubscription.objects.filter(pk=subscription.pk).exists())

        # assert that the user is not deleted after the subscription model
        self.assertTrue(User.objects.filter(pk=new_user.pk).exists())
    
    
    def test_updating_subscription_information(self):
        """
        Test updating subscription data without affecting the user.
        """
        new_user = create_test_user()
        self.assertIsNotNone(new_user)

        subscription = NewsletterSubscription.objects.create(
            title="Initial subscription title",
            user=new_user,
            email="subscription_email@example.com",
            subscribed_on=timezone.now(),
            unsubscribed=False,
        )

        # Update the subscription's title
        subscription.title = "Updated subscription title"
        subscription.save()

        subscription.refresh_from_db()
        self.assertEqual(subscription.title, "Updated subscription title")

        # Verify the user was not affected
        self.assertTrue(get_user_model().objects.filter(pk=new_user.pk).exists())

    def test_subscription_creation_without_user(self):
        """
        Test that creating a subscription without an associated user raises an IntegrityError,
        ensuring the transaction is properly managed.
        """
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                NewsletterSubscription.objects.create(
                    title="Test subscription without user",
                    email="subscription_email@example.com",
                    subscribed_on=timezone.now(),
                    unsubscribed=False,
                )
        
    def tearDown(self):
        """Clean up test data after each test method is executed."""
        NewsletterSubscription.objects.all().delete()
     