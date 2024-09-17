from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.test import TestCase



from authentication.models import BanUser, User
from utils.dates import calculate_days_between_dates


def create_permanently_banned_user(username="forever_banned", 
                                    email="forever_banned@example.com", 
                                    password="trouble", 
                                    ban_reason="Causing trouble"):
    """
    Creates a user with a permanent ban.
    """
    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email
    )
    
    # When no start date or expiry date is added, the ban is permanent
    user_ban_record = BanUser.objects.create(user=user, ban_reason=ban_reason)
    user_ban_record.ban()
    
    return user_ban_record


def create_temporarily_banned_user(ban_start, 
                                    ban_end, 
                                    username="temp_banned_user", 
                                    email="temp_banned@example.com", 
                                    password="trouble", 
                                    ban_reason="Causing trouble"):
    """
    Creates a user with a temporary ban for a specified date range.
    """
    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email
    )
    
    user_ban_record = BanUser.objects.create(user=user, ban_reason=ban_reason)
    user_ban_record.ban_for_date_range(ban_start, ban_end)
    
    return user_ban_record


def create_banned_user_for_days(username="banned_for_days_user",
                                 email="banned_for_days@example.com",
                                 password="trouble", 
                                 ban_reason="Causing trouble",
                                 days_to_ban=30):
    """
    Creates a user with a temporary ban for a specified number of days.
    """
    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email
    )
    
    user_ban_record = BanUser.objects.create(user=user, ban_reason=ban_reason)
    user_ban_record.ban_for_x_amount_of_days(num_of_days_to_ban=days_to_ban)
    
    return user_ban_record


class CustomBanUserModelTestCase(TestCase):
    """
    Test case for the BanUser model, focusing on different ban scenarios like 
    permanent bans, temporary bans with date ranges, and bans for a specific number of days.
    """
    
    def setUp(self):
        """
        Set up the initial test data for each test case, including users and 
        different types of ban records (permanent, temporary, and days-based bans).
        """
        self.BAN_START_DATE = datetime.now()
        self.BAN_EXPIRES_ON = self.BAN_START_DATE + timedelta(days=30)
        self.BAN_REASON = "Causing trouble"
        self.BAN_USERNAME = "user".title()
        self.BAN_EMAIL = "user@example.com"
  

        # Creating users with different ban types
        self.permanently_banned_user = create_permanently_banned_user()
        self.temporarily_banned_user = create_temporarily_banned_user(ban_start=self.BAN_START_DATE, ban_end=self.BAN_EXPIRES_ON)
        self.temp_banned_user_for_days = create_banned_user_for_days()
    
    def test_creation_count(self):
        """Ensure the correct number of User and BanUser objects are created."""
        
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(BanUser.objects.count(), 3)
        
    def test_permanent_ban_attributes(self):
        """
        Verify that the permanent ban is created with the correct attributes, 
        ensuring no start or expiration date is set for permanent bans.
        """
        perm_banned_user = User.objects.filter(email="forever_banned@example.com").first()
        self.assertIsNotNone(perm_banned_user)

        banned_user = BanUser.objects.filter(user=perm_banned_user).first()
        self.assertIsNotNone(banned_user)

        self.assertEqual(banned_user.ban_reason, self.BAN_REASON)
        self.assertIsNone(banned_user.ban_expires_on)
        self.assertIsNone(banned_user.ban_start_date)
        self.assertEqual(banned_user.user, perm_banned_user)
    
    def test_temp_permanent_ban_date_range_attributes(self):
        """
        Test temporary bans with a start and end date. Ensure the date fields are 
        set correctly for users banned for a specific period.
        """
        temp_banned_user = User.objects.filter(email="temp_banned@example.com").first()
        self.assertIsNotNone(temp_banned_user)

        user_ban_record = BanUser.objects.filter(user=temp_banned_user).first()
        self.assertIsNotNone(user_ban_record)

        # Compare date fields down to the minute, ignoring seconds and microseconds
        self.assertEqual(user_ban_record.ban_expires_on.replace(microsecond=0, second=0), 
                         make_aware(self.BAN_EXPIRES_ON.replace(microsecond=0, second=0)))
        self.assertEqual(user_ban_record.ban_start_date.replace(microsecond=0, second=0), 
                         make_aware(self.BAN_START_DATE.replace(microsecond=0, second=0)))

        self.assertEqual(user_ban_record.user, temp_banned_user)
    
    def test_temp_days_ban_attributes(self):
        """
        Test the creation of bans for a specified number of days. 
        Ensure the correct start and expiration dates are set.
        """
        temp_banned_user = User.objects.filter(email="banned_for_days@example.com").first()
        self.assertIsNotNone(temp_banned_user)

        user_ban_record = BanUser.objects.filter(user=temp_banned_user).first()
        self.assertIsNotNone(user_ban_record)

        ban_expires_date = self.BAN_START_DATE + timedelta(days=30)

        # Ensure the start date and expiration date are correct (ignoring seconds/microseconds)
        self.assertAlmostEqual(user_ban_record.ban_start_date.replace(microsecond=0, second=0), 
                         make_aware(self.BAN_START_DATE.replace(microsecond=0, second=0)))
        self.assertAlmostEqual(user_ban_record.ban_expires_on.replace(microsecond=0, second=0), 
                         make_aware(ban_expires_date.replace(microsecond=0, second=0)))

        self.assertEqual(user_ban_record.user, temp_banned_user)

    def test_user_is_permanently_banned(self):
        """Test if the ban model marks the user as permanently banned"""
        
        user = User.get_by_email(email=self.permanently_banned_user.user.email)
        self.assertIsNotNone(user)
        self.assertTrue(user.is_banned)
        self.assertFalse(user.is_temp_ban)
    
   
    def test_temporary_ban_applied_correctly_with_date_range(self):
        """
        Test that a temporary ban is correctly applied on a user account when a date range 
        ban is is used.
        
        Verifies that the user is correctly flagged as temporarily banned and that their 
        ban status reflects the use of a date range for the ban.
        """
        
        user = User.get_by_email(email=self.temporarily_banned_user.user.email)
        self.assertIsNotNone(user)
        self.assertFalse(user.is_banned)  
        self.assertTrue(user.is_temp_ban)  

    def test_temporary_ban_applied_correctly_for_days(self):
        """
        Test that a temporary ban is correctly applied when a user is banned for a 
        specified number of days.
        
        Verifies that the user is correctly flagged as temporarily banned and that their 
        ban status reflects the correct duration of the ban.
        """
        
        user = User.get_by_email(email=self.temp_banned_user_for_days.user.email)
        self.assertIsNotNone(user)
        self.assertFalse(user.is_banned)  
        self.assertTrue(user.is_temp_ban)

    
    def test_no_new_ban_when_permanent_ban_in_place(self):
        """Test that a new ban cannot be implemented if there is already one in place"""
        
    
        user = User.get_by_email(email=self.permanently_banned_user.user.email)
        
        self.assertIsNotNone(user)
        self.assertTrue(user.is_banned)     # Ensure the user has a permanent ban before attempting a new one
        self.assertFalse(user.is_temp_ban)
        
        user_ban_record = BanUser.objects.filter(user=user).first()
        
        self.assertIsNotNone(user_ban_record, "This should not be empty")

        # Attempt to apply a temporary ban on a user with a permanent ban
        resp = user_ban_record.ban_for_x_amount_of_days(num_of_days_to_ban=7)
        self.assertEqual(resp, "User already has a permanent ban")
        
        user.refresh_from_db()
        
        # # Ensure that the user's ban status has not been modified
        self.assertTrue(user.is_banned)
        self.assertFalse(user.is_temp_ban)

    def test_no_new_ban_when_temp_ban_exists_using_date_range(self):
        """
        Test that a new temporary ban cannot be applied if a user already has an existing 
        temporary ban set using a date range.
        
        Verifies that attempting to apply another temporary ban to a user who already has 
        a temporary ban results in a notification that the user is already banned and that 
        the user's existing ban status remains unchanged.
        """
        
        user = User.get_by_email(email=self.temporarily_banned_user.user.email)
        
        self.assertIsNotNone(user)
        self.assertFalse(user.is_banned)     # Ensure the user is flagged as temporarily banned
        self.assertTrue(user.is_temp_ban)
        
        user_ban_record = BanUser.objects.filter(user=user).first()
        
        self.assertIsNotNone(user_ban_record, "This should not be empty")

        # Attempt to apply a temporary ban on a user who already has a temporary ban
        resp = user_ban_record.ban_for_x_amount_of_days(num_of_days_to_ban=7)
        self.assertEqual(resp, "User already has a temporary ban")
        
        user.refresh_from_db()
        
        # Ensure that the user's ban status has not been modified
        self.assertFalse(user.is_banned)
        self.assertTrue(user.is_temp_ban)

    def test_no_new_ban_when_temp_ban_exists_using_num_of_days(self):
        """
        Test that a new temporary ban cannot be applied if a user already has an existing 
        temporary ban set using number of days.
        
        Verifies that attempting to apply another temporary ban to a user who already has 
        a temporary ban results in a notification that the user is already banned and that 
        the user's existing ban status remains unchanged.
        """
        
        user = User.get_by_email(email=self.temp_banned_user_for_days.user.email)
        
        self.assertIsNotNone(user)
        self.assertFalse(user.is_banned)     # Ensure the user is flagged as temporarily banned
        self.assertTrue(user.is_temp_ban)
        
        user_ban_record = BanUser.objects.filter(user=user).first()
        
        self.assertIsNotNone(user_ban_record, "This should not be empty")

        # Attempt to apply a temporary ban on a user who already has a temporary ban
        resp = user_ban_record.ban_for_x_amount_of_days(num_of_days_to_ban=7)
        self.assertEqual(resp, "User already has a temporary ban")
        
        user.refresh_from_db()
        
        # Ensure that the user's ban status has not been modified
        self.assertFalse(user.is_banned)
        self.assertTrue(user.is_temp_ban)
        

    def test_permanent_ban_does_not_expire(self):
        """Test that a permanent ban doesn't expires regardless if a expire date is added"""
        
        regular_user = User.objects.create(username="new user", 
                                                password="new password", 
                                                email="new_user@example.com")
        
        BAN_START_DATE = make_aware(self.BAN_START_DATE)
        expired_user_ban_record = BanUser.objects.create(user=regular_user, 
                                                    ban_reason="Temporary ban", 
                                                    ban_start_date=BAN_START_DATE,
                                                    ban_expires_on=BAN_START_DATE - timedelta(days=1)  # Already expired
                                                    
                                                 )
        
        expired_user_ban_record.ban()
        expired_user_ban_record.refresh_from_db()
        
        self.assertTrue(regular_user.is_banned)
        self.assertFalse(regular_user.is_temp_ban)
        
        self.assertFalse(expired_user_ban_record.has_ban_expired())
    
    def test_temp_ban_expires(self):
        """Test that a temp ban correctly reflects expiration status"""
        
        regular_user = User.objects.create_user(
            username="new_user", 
            password="new_password", 
            email="new_user@example.com"
        )
        
        # Create a temporary ban that will expire soon
        BAN_START_DATE      = make_aware(datetime.now())
        ban_expiration_date = BAN_START_DATE + timedelta(days=1)
        
        expired_user_ban_record = BanUser.objects.create(
            user=regular_user, 
            ban_reason="Temporary ban", 
             ban_start_date=BAN_START_DATE,
            ban_expires_on=ban_expiration_date
        )
        
        # Issue a temp ban that should expire 2 days ago
        expired_user_ban_record.ban_for_x_amount_of_days(
            num_of_days_to_ban=-2,  # Negative days to simulate an expired ban
            save=True
        )
        
        regular_user.refresh_from_db()
        expired_user_ban_record.refresh_from_db()
        
                                   
        self.assertFalse(regular_user.is_banned)             # Check that the user is not permanently banned
        self.assertTrue(regular_user.is_temp_ban)            # Check that the user is marked as having a temporary ban
        self.assertTrue(expired_user_ban_record.has_ban_expired())  # Check that the ban status correctly reflects expiration

    def test_ban_method_marks_user_as_banned(self):
        """Test if the ban method properly marks the user as banned"""
        
        regular_user = User.objects.create(username="new user", 
                                           password="new password", 
                                           email="new_user@example.com")
        
       
        user_ban_record = BanUser.objects.create(user=regular_user, ban_reason="Temporary ban")  # no dates - means a permanent ban when the ban() is called                          
        user_ban_record.ban()
      
        regular_user.refresh_from_db()
        self.assertTrue(regular_user.is_banned)

    def test_ban_username_property(self):
        """Test if the ban username property returns the correct username"""
        self.assertEqual(self.permanently_banned_user.username, "Forever_Banned")
    
    def test_ban_duration_days_method(self):
        """Test if the method returns the correct amount of days for a given ban"""
        
        # call the user who was issued the ban using the date range
        EXPECTED_NUM_OF_DAYS_BANNED = calculate_days_between_dates(self.BAN_EXPIRES_ON, self.BAN_START_DATE)
        self.assertEqual(self.temporarily_banned_user.ban_duration_days, EXPECTED_NUM_OF_DAYS_BANNED)
    
    def test_remaining_days_method(self):
        """Test if the method returns the correct amount of days remaining for a ban"""
        
        # call the user who was banned using num of days
        EXPECTED_NUM_OF_DAYS_REMAINIING = calculate_days_between_dates(self.BAN_EXPIRES_ON, self.BAN_START_DATE)  
        self.assertAlmostEqual(EXPECTED_NUM_OF_DAYS_REMAINIING, self.temp_banned_user_for_days.remaining_days)
       
        # test if returns 0 when no more days are remaining
        regular_user = User.objects.create_user(username="user10", password="new_password",  email="new_user10@example.com")
       
        expired_user_ban_record = BanUser.objects.create(user=regular_user, 
                                                  ban_reason="Temporary ban",  
                                                )
        
        # Issue a temp ban that should expire 2 days ago
        expired_user_ban_record.ban_for_x_amount_of_days(num_of_days_to_ban=-2)  # Negative days to simulate an expired ban
        self.assertEqual(expired_user_ban_record.remaining_days, 0)
        
    def test_unban_method_for_permanent_ban(self):
        """Test if the un_ban method correctly unbans a permanent ban"""
        
        user = User.get_by_username(username=self.permanently_banned_user.username)
        
        self.assertIsNotNone(user, self.permanently_banned_user.username)
        self.assertTrue(user.is_banned)  
        self.assertFalse(user.is_temp_ban)
                
        user_ban_record = BanUser.objects.filter(user=user).first()
        
        self.assertTrue(user_ban_record, "The ban user should be available")
        
        user_ban_record.un_ban()
        user.refresh_from_db()
        
        # assert that the ban has been lifted
        self.assertFalse(user.is_banned)
    
    def test_unban_method_for_temporary_ban(self):
        """Test if the un_ban method correctly unbans a temporary ban"""
        
        user = User.get_by_username(username=self.temporarily_banned_user.username)
        
        self.assertIsNotNone(user, self.temporarily_banned_user.username)
        self.assertFalse(user.is_banned)  
        self.assertTrue(user.is_temp_ban)
        
        user_ban_record = BanUser.objects.filter(user=user).first()
        
        self.assertTrue(user_ban_record, "The ban user should be available")
        
        user_ban_record.un_ban()
        user.refresh_from_db()
        
        # assert that the ban has been lifted
        self.assertFalse(user.is_banned)
    
    
    def test_unban_method_no_ban_record(self):
        """Test if the un_ban method handles the case where no ban record exists for the user"""
        
        regular_joe = User.objects.create_user(
                            username="regular joe", 
                            password="password", 
                            email="regular_joe@example.com"
                        )
        
        
        self.assertFalse(regular_joe.is_banned)
        
        user_ban_record = BanUser.objects.filter(user=regular_joe).first()
    
        self.assertIsNone(user_ban_record, "The ban user record should not exist")
        
        # Attempt to call un_ban() on a non-existent ban record
        if user_ban_record:
            user_ban_record.un_ban()
        
        regular_joe.refresh_from_db()
        
        # Assert that the user's ban status remains unchanged
        self.assertFalse(regular_joe.is_banned)

    
    def test_user_is_unbanned_when_ban_record_is_deleted(self):
        """
        Test that a user is automatically unbanned when their associated ban record is deleted.

        This test creates a user, applies a ban to them, and verifies that the ban is active. 
        After deleting the ban record, it ensures that the user's ban status is updated, 
        confirming they are no longer banned.
        """
        # Create a user
        jane_doe = User.objects.create_user(
            username="jane doe", 
            password="password", 
            email="jane_doe@example.com"
        )

        # Assert that the user is not banned initially
        self.assertFalse(jane_doe.is_banned)

        # Apply a ban to the user
        user_ban_record = BanUser.objects.create(user=jane_doe, ban_reason=self.BAN_REASON)
        user_ban_record.ban()

    
        jane_doe.refresh_from_db()
        self.assertTrue(jane_doe.is_banned)

        user_ban_record.delete()

        jane_doe.refresh_from_db()
        self.assertFalse(jane_doe.is_banned)

    def tearDown(self) -> None:
        User.objects.all().delete()
        BanUser.objects.all().delete()
        
   