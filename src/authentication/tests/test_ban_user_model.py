from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.test import TestCase

from django.contrib.auth import get_user_model

from authentication.models import BanUser
from utils.dates import calculate_days_between_dates



class CustomBanUserModelTestCase(TestCase):
    
    def setUp(self):
        self.BAN_START_DATE  = make_aware(datetime.now())
        self.BAN_EXPIRES_ON  = self.BAN_START_DATE + timedelta(days=30)
        self.BAN_REASON      = "Causing trouble"
        self.BAN_USERNAME    = "user".title()
        self.BAN_EMAIL       = "user@example.com"
        self.User            = get_user_model()
      
        # Create a regular user 
        self.regular_user = self.User.objects.create_user(
            username=self.BAN_USERNAME, 
            password="password", 
            email="user@example.com"
        )
             
        self.ban_user = BanUser.objects.create(user=self.regular_user, 
                                               ban_reason=self.BAN_REASON, 
                                               ban_expires_on=self.BAN_EXPIRES_ON,
                                                ban_start_date=self.BAN_START_DATE,
                                               )
                                              
        self.ban_user.ban()
        
    def test_creation_count(self):
        """Test the number of objects created"""
        self.assertEqual(self.User.objects.count(), 1)  
        self.assertEqual(BanUser.objects.count(), 1)  # Only one ban created
        
    def test_ban_attributes(self):
        """Test the ban model is created with correct fields"""
        
        self.assertEqual(self.ban_user.ban_reason, self.BAN_REASON)
        self.assertEqual(self.ban_user.ban_expires_on, self.BAN_EXPIRES_ON)
        self.assertEqual(self.ban_user.ban_start_date, self.BAN_START_DATE)
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
                                                      ban_start_date=self.BAN_START_DATE,
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
        
        self.regular_user.refresh_from_db()
        
        # Ensure that the user's ban status has not been modified
        self.assertTrue(self.regular_user.is_banned)
        self.assertFalse(self.regular_user.is_temp_ban)

    def test_no_new_ban_when_a_temp_ban_in_place(self):
        """Test that a new ban cannot be implemented if there is already one in place"""
        
        user = self.User.objects.create(username="temp ban user", 
                                                password="password", 
                                                email="temp_user@example.com")
        
        temp_ban_user = BanUser.objects.create(user=user, 
                                                ban_reason=self.BAN_REASON, 
                                                ban_expires_on=self.BAN_EXPIRES_ON,
                                                ban_start_date=self.BAN_START_DATE,
                                                )

        temp_ban_user.ban_for_x_amount_of_days(self.BAN_REASON)
        
        # Attempt to apply a new temporary ban on a user who already has a temporary ban
        resp = temp_ban_user.ban_for_x_amount_of_days(ban_reason="Temporary ban", num_of_days_to_ban=7)
        self.assertEqual(resp, "User already has a temporary ban")
        
        user.refresh_from_db()
        
        # Ensure that the user's ban status has not been modified
        self.assertFalse(user.is_banned)
        self.assertTrue(user.is_temp_ban)

    def test_permanent_ban_does_not_expire(self):
        """Test that a permanent ban doesn't expires regardless if a expire date is added"""
        
        regular_user = self.User.objects.create(username="new user", 
                                                password="new password", 
                                                email="new_user@example.com")
        expired_ban_user = BanUser.objects.create(
            user=regular_user, 
            ban_reason="Temporary ban", 
            ban_start_date=self.BAN_START_DATE,
            ban_expires_on=self.BAN_START_DATE - timedelta(days=1)  # Already expired
            
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
        ban_expiration_date = self.BAN_START_DATE + timedelta(days=1)
        expired_ban_user = BanUser.objects.create(
            user=regular_user, 
            ban_reason="Temporary ban", 
             ban_start_date=self.BAN_START_DATE,
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

    def test_ban_username_property(self):
        """Test if the ban username property returns the correct username"""
        self.assertEqual(self.ban_user.username, self.BAN_USERNAME)
    
    def test_ban_duration_days_method(self):
        """Test if the method returns the correct amount of days for a given ban"""
        
        EXPECTED_NUM_OF_DAYS_BANNED = calculate_days_between_dates(self.BAN_EXPIRES_ON, self.BAN_START_DATE)
        self.assertEqual(self.ban_user.ban_duration_days, EXPECTED_NUM_OF_DAYS_BANNED)
    
    def test_remaining_days_method(self):
        """Test if the method returns the correct amount of days remaining for a ban"""
        
        EXPECTED_NUM_OF_DAYS_REMAINIING = calculate_days_between_dates(self.BAN_EXPIRES_ON, self.BAN_START_DATE) - 1 # not including the start date
        self.assertEqual(self.ban_user.remaining_days, EXPECTED_NUM_OF_DAYS_REMAINIING)
        
        # test if returns 0 when no more days are remaining
        regular_user = self.User.objects.create_user(
            username="user10", 
            password="new_password", 
            email="new_user10@example.com"
        )
       
        # Create a temporary ban that has expired
        ban_expiration_date = self.BAN_START_DATE 
        expired_ban_user = BanUser.objects.create(
            user=regular_user, 
            ban_reason="Temporary ban", 
             ban_start_date=self.BAN_START_DATE,
            ban_expires_on=ban_expiration_date
        )
        
        # Issue a temp ban that should expire 2 days ago
        expired_ban_user.ban_for_x_amount_of_days(
            ban_reason="Expired temporary ban", 
            num_of_days_to_ban=-2,  # Negative days to simulate an expired ban
            save=True
        )
        self.assertEqual(expired_ban_user.remaining_days, 0)
        
    def test_unban_method_for_permanent_ban(self):
        """Test if the un_ban method correctly unbans a permanent ban"""
        
        # assert that a user is banned
        self.assertTrue(self.regular_user.is_banned)
        
        ban_user = BanUser.objects.filter(user=self.regular_user).first()
        
        self.assertTrue(ban_user, "The ban user should be available")
        
        ban_user.un_ban()
        self.regular_user.refresh_from_db()
        
        # assert that the ban has been lifted
        self.assertFalse(self.regular_user.is_banned)
    
    def test_unban_method_for_temporary_ban(self):
        """Test if the un_ban method correctly unbans a temporary ban"""
        
        # Create a regular user 
        new_user = self.User.objects.create_user(
            username="some user", 
            password="password", 
            email="some_user@example.com"
        )

        ban_user = BanUser.objects.create(user=new_user, 
                                          ban_reason=self.BAN_REASON, 
                                          ban_expires_on=self.BAN_EXPIRES_ON,
                                          ban_start_date=self.BAN_START_DATE,
                                          )
        
        ban_user.ban_for_x_amount_of_days(self.BAN_REASON)
        
        # assert the user has a temporary ban placed on them
        self.assertTrue(new_user.is_temp_ban)

        ban_user.un_ban()
        
        new_user.refresh_from_db()
        
        # assert that the ban has been lifted
        self.assertFalse(new_user.is_temp_ban)
    
    
    def test_unban_method_no_ban_record(self):
        """Test if the un_ban method handles the case where no ban record exists for the user"""
        
        regular_joe = self.User.objects.create_user(
                            username="regular joe", 
                            password="password", 
                            email="regular_joe@example.com"
                        )
        
        
        self.assertFalse(regular_joe.is_banned)
        
      
        ban_user = BanUser.objects.filter(user=regular_joe).first()
    
        self.assertIsNone(ban_user, "The ban user record should not exist")
        
        # Attempt to call un_ban() on a non-existent ban record
        if ban_user:
            ban_user.un_ban()
        
       
        self.regular_user.refresh_from_db()
        
        # Assert that the user's ban status remains unchanged
        self.assertFalse(regular_joe.is_banned)

        
    def tearDown(self) -> None:
        self.User.objects.all().delete()
        BanUser.objects.all().delete()
        
   