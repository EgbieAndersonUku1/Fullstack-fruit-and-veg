from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from django.test import TestCase

from django.contrib.auth import get_user_model


class CustomUserModelTestCase(TestCase):
    
    def setUp(self):
        self.User = get_user_model()

        # Create a regular user
        self.user = self.User.objects.create_user(
            username="user", 
            password="password", 
            email="user@example.com"
        )
        
        # Create a superuser
        self.super_user = self.User.objects.create_superuser(
            username="super_user", 
            password="password", 
            email="super_user@example.com"
        )
    
    def test_creation_count(self):
        """Test the number of objects created"""
        
        # There should be a normal user and a superuser
        query_set = self.User.all()
        self.assertEqual(query_set.count(), 2)
        
    def test_user_creation(self):
        """Test if the regular user was created correctly."""
        user = self.User.objects.get(username="user")
        
        # Check if user exists
        self.assertIsNotNone(user)
        
        # Check permissions
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_admin)  # Directly checking is_admin since it's part of the model
        self.assertFalse(user.is_staff)
        
        # Check values
        self.assertEqual(user.username, "user")
        self.assertEqual(user.email, "user@example.com")
        
        # Test if the password is hashed and correct
        self.assertNotEqual(user.password, "password")  # Ensure the password is not stored as plaintext
        self.assertTrue(user.check_password("password"))  # Ensure the password is correct

    def test_super_user_creation(self):
        """Test if the superuser was created correctly."""
        super_user = self.User.objects.get(username="super_user")
        
        # Check if superuser exists
        self.assertIsNotNone(super_user)
        
        # Check permissions
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_admin) # Directly checking is_admin since it's part of the model
        self.assertTrue(super_user.is_staff)
        
        # Check values
        self.assertEqual(super_user.username, "super_user")
        self.assertEqual(super_user.email, "super_user@example.com")
        
        # Test if the password is hashed and correct
        self.assertNotEqual(super_user.password, "password")  # Ensure the password is not stored as plaintext
        self.assertTrue(super_user.check_password("password"))  # Ensure the password is correct and in hash format

    def test_username_uniqueness(self):
        """Test that creating a user with a duplicate username raises an IntegrityError."""

        
        with self.assertRaises(IntegrityError):
            self.User.objects.create(email="egbie@example.com",
                                     username="user", # duplicate name
                                     password="password",
                                     )
    
    def test_email_uniqueness(self):
        """Test that creating a user with a duplicate email raises an IntegrityError."""

        
        with self.assertRaises(IntegrityError):
            self.User.objects.create(email="super_user@example.com", # duplicate email
                                     username="user", 
                                     password="password",
                                     )
    
    def test_get_by_email_method(self):
        """Test the get_by_email method found on the user model"""
        
        user = self.User.get_by_email("super_user@example.com")
        self.assertIsNotNone(user)
        
    def test_get_by_username_method(self):
        """Test the get_by_username method found on the user model"""
        
        user = self.User.get_by_username("user")
        self.assertIsNotNone(user)
    
    def test_str_method(self):
        """Test the __str__ method returns the user's email."""
        self.assertEqual(str(self.user), "user@example.com")
        self.assertEqual(str(self.super_user), "super_user@example.com")
        
    
    def test_if_verification_data_is_set(self):
        """Test if the verification code and dates are set correctly on the user model"""
        
        verification_code = "some-random-code-that-I-made-up"
        expiry_minutes = 2
        self.user.set_verification_code(verification_code, expiry_minutes=expiry_minutes)
        
        # Retrieve the user from the db to ensure data consistency
        user = self.User.get_by_username("user")
        
        # Check that verification data exists and contains the correct fields
        self.assertIsNotNone(user.verification_data)
        self.assertIn("verification_code", user.verification_data)
        self.assertIn("date_sent", user.verification_data)
        self.assertIn("expiry_date", user.verification_data)

        # Verify that the verification code matches
        self.assertEqual(user.verification_data.get("verification_code"), verification_code)
        
        # Verify date_sent and expiry_date
        date_sent_str = user.verification_data.get("date_sent")
        expiry_date_str = user.verification_data.get("expiry_date")
        
        # Parse the date strings back into datetime objects
        date_sent = datetime.fromisoformat(date_sent_str)
        expiry_date = datetime.fromisoformat(expiry_date_str)

        # Check if date_sent is approximately now (allowing for slight delay in code execution)
        self.assertAlmostEqual(date_sent, datetime.now(), delta=timedelta(seconds=5))

        # Check if expiry_date is date_sent + expiry_minutes
        expected_expiry_date = date_sent + timedelta(minutes=expiry_minutes)
        self.assertEqual(expiry_date, expected_expiry_date)
    
    def test_if_verification_code_is_correct(self):
        """Test if the verification code is set to the user model"""
        
        verification_code = "some-random-code-that-I-made-up"
        self.user.set_verification_code(verification_code, expiry_minutes=2)
        
        # call the model from the db and not the created one in the constructor
        user = self.User.get_by_username("user")
     
        # check that code matches the given code
        self.assertEqual(user.verification_data.get("verification_code"), verification_code)
    
    def test_is_verification_code_valid_returns_true_if_code_not_expired(self):
        """
        Test that `is_verification_code_valid` returns True if the verification code is not expired.
        """
        
        # not expired
        verification_code = "some-random-code-that-I-made-up"
        expiry_minutes = 4
        self.user.set_verification_code(verification_code, expiry_minutes=expiry_minutes)
        
        # Retrieve the user from the db to ensure data consistency
        user = self.User.get_by_username("user")
        
        resp = user.is_verification_code_valid(verification_code)[0]

        self.assertTrue(resp)

    def test_user_is_not_created_with_verified_email(self):
        """
        Test that the user's email is not verified upon creation.
        """
        self.assertFalse(self.user.is_email_verified)
    
    def test_user_is_not_banned_upon_creation(self):
        """
        Test that a user is not banned when initially created.
        """
        self.assertFalse(self.user.is_banned)

    def test_clear_verification_data_method(self):
        """Test if the method successfully clears user verification data"""

        # set up 
        verification_code = "some-random-code-that-I-made-up"
        expiry_minutes = 4
        self.user.set_verification_code(verification_code, expiry_minutes=expiry_minutes)
        
        # Retrieve the user from the db to ensure data consistency
        user = self.User.get_by_username("user")
        
        # verify that verification data exists
        self.assertTrue(user.verification_data)
        
        # wipe the data
        user.clear_verification_data()
        
        # call the method after wiping the data
        self.assertFalse(user.verification_data)
    
    def test_user_is_banned_after_ban_action(self):
        """
        Test that a user becomes banned after a ban action is applied.
        """
        self.user.ban()  
        self.assertTrue(self.user.is_banned)

    def test_un_ban_user(self):
        """
        Test that a user becomes unbanned after a ban action is applied.
        """
        # apply the ban and test if is banned
        self.user.ban()
        self.assertTrue(self.user.is_banned)
        
        # unban the user
        self.user.un_ban()
        self.assertFalse(self.user.is_banned)
    
    def test_mark_email_as_verified_method(self):
        """Test if the method successfully marks the email as verified"""
        
        # Test if the email is unverifed first
        self.assertFalse(self.user.is_email_verified)
        
        self.user.mark_email_as_verified()
        
        self.assertTrue(self.user.is_email_verified)
        
        
    def test_does_user_exists_method(self):
        """Test if the user exists by calling the method within the class"""
        
        # call a user that exists
        self.assertTrue(self.User.does_user_exists(username="user"))
        
        # call a user that doesn't exists
        self.assertFalse(self.User.does_user_exists(username="user_does_exists"))