from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.test import TestCase

from django.contrib.auth import get_user_model

from authentication.models import BanUser
from utils.converter import string_to_date


class CustomBanUserModelTestCase(TestCase):
    
    def setUp(self):
        self.current_date    = make_aware(datetime.now())
        self.BAN_EXPIRES_ON  = self.current_date + timedelta(days=30)
        self.BAN_REASON      = "Causing trouble"
        self.User            = get_user_model()
      
        # Create a regular user and a superuser
        self.regular_user = self.User.objects.create_user(
            username="user", 
            password="password", 
            email="user@example.com"
        )
        
        self.super_user = self.User.objects.create_superuser(
            username="super_user", 
            password="password", 
            email="super_user@example.com"
        )
        
        self.ban_user = BanUser.objects.create(user=self.regular_user, 
                                               ban_reason=self.BAN_REASON, 
                                               ban_expires_on=self.BAN_EXPIRES_ON,
                                                ban_start_date=self.current_date
                                               )
                                              
        self.ban_user.ban()
      
    def test_creation_count(self):
        """Test the number of objects created"""
        self.assertEqual(self.User.objects.count(), 2)  # One regular user, one superuser
        self.assertEqual(BanUser.objects.count(), 1)  # Only one ban created
        
    def test_ban_attributes(self):
        """Test the ban model is created with correct fields"""
        
        self.assertEqual(self.ban_user.ban_reason, self.BAN_REASON)
        self.assertEqual(self.ban_user.ban_expires_on, self.BAN_EXPIRES_ON)
        self.assertEqual(self.ban_user.ban_start_date, self.current_date)
        self.assertEqual(self.ban_user.user, self.regular_user)
    
    def test_user_is_permanently_banned(self):
        """Test if the ban model marks the user as permanently banned"""
        
        self.assertTrue(self.regular_user.is_banned)
        self.assertFalse(self.regular_user.is_temp_ban)
    
    def test_temporary_ban(self):
        """Test if a temporary ban is applied correctly"""
        
        new_regular_user = self.User.objects.create(username="regular user", 
                                                password="password", 
                                                email="regular_user@example.com")
        
        ban_regular_user = BanUser.objects.create(user=new_regular_user, 
                                                      ban_reason=self.BAN_REASON, 
                                                      ban_expires_on=self.BAN_EXPIRES_ON,
                                                      ban_start_date=self.current_date,
                                                      )
        
        ban_regular_user.ban_for_x_amount_of_days(ban_reason="Temporary ban", num_of_days_to_ban=7)
        
        ban_regular_user.refresh_from_db()
        self.assertTrue(new_regular_user.is_temp_ban)
        self.assertFalse(new_regular_user.is_banned)  # Ensure it's not a permanent ban
    
    def test_no_new_ban_when_permanent_ban_in_place(self):
        """Test that a new ban cannot be implemented if there is already one in place"""
        
        # Ensure the user has a permanent ban before attempting a new one
        self.assertTrue(self.regular_user.is_banned)

        # Attempt to apply a temporary ban on a user with a permanent ban
        resp = self.ban_user.ban_for_x_amount_of_days(ban_reason="Temporary ban", num_of_days_to_ban=7)
        self.assertEqual(resp, "User already has a permanent ban")
        
        # Ensure that the user's ban status has not been modified
        self.assertTrue(self.regular_user.is_banned)
        self.assertFalse(self.regular_user.is_temp_ban)

    def test_permanent_ban_does_not_expire(self):
        """Test that a permanent ban doesn't expires regardless if a expire date is added"""
        
        regular_user = self.User.objects.create(username="new user", 
                                                password="new password", 
                                                email="new_user@example.com")
        expired_ban_user = BanUser.objects.create(
            user=regular_user, 
            ban_reason="Temporary ban", 
            ban_start_date=self.current_date,
            ban_expires_on=self.current_date - timedelta(days=1)  # Already expired
            
        )
        
        expired_ban_user.ban()
        expired_ban_user.refresh_from_db()
        
        self.assertTrue(regular_user.is_banned)
        self.assertFalse(regular_user.is_temp_ban)
        
        self.assertFalse(expired_ban_user.has_ban_expired())
    
    def test_temp_ban_expires(self):
        """Test that a temp ban correctly reflects expiration status"""
        
        regular_user = self.User.objects.create_user(
            username="new_user", 
            password="new_password", 
            email="new_user@example.com"
        )
        
        # Create a temporary ban that will expire soon
        ban_expiration_date = self.current_date + timedelta(days=1)
        expired_ban_user = BanUser.objects.create(
            user=regular_user, 
            ban_reason="Temporary ban", 
             ban_start_date=self.current_date,
            ban_expires_on=ban_expiration_date
        )
        
        # Issue a temp ban that should expire 2 days ago
        expired_ban_user.ban_for_x_amount_of_days(
            ban_reason="Expired temporary ban", 
            num_of_days_to_ban=-2,  # Negative days to simulate an expired ban
            save=True
        )
        
        regular_user.refresh_from_db()
        expired_ban_user.refresh_from_db()
        
        # Check that the user is not permanently banned
        self.assertFalse(regular_user.is_banned)
        
        # Check that the user is marked as having a temporary ban
        self.assertTrue(regular_user.is_temp_ban)
        
        # Check that the ban status correctly reflects expiration
        self.assertTrue(expired_ban_user.has_ban_expired())

    def test_ban_method_marks_user_as_banned(self):
        """Test if the ban method properly marks the user as banned"""
        
        self.ban_user.ban()
        self.ban_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_banned)

    def tearDown(self) -> None:
        self.User.objects.all().delete()
        BanUser.objects.all().delete()