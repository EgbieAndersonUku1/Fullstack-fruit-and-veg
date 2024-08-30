from django.test import TestCase

from ..forms.register_form import RegisterForm


class RegisterFormTest(TestCase):

    def test_register_form_valid_data(self):
        """Test that form is valid with all required fields properly filled."""
        
        form_data = {
            "username": "username",
            "email": "email@example.com",
            "password": "password",
            "confirm_password": "password", 
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        """Test that form is invalid when no data is provided."""
        form_data = {}
        form      = RegisterForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Ensure all fields have errors

    def test_register_form_missing_required_attributes(self):
        """Test that form is invalid when required fields are missing or empty."""

        # Test missing username
        form_data = {
            "username": "",
            "email": "email@example.com",
            "password": "password",
            "confirm_password": "password",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

        # Test missing email
        form_data = {
            "username": "username",
            "email": "",
            "password": "password",
            "confirm_password": "password",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

        # Test missing password
        form_data = {
            "username": "username",
            "email": "email@example.com",
            "password": "",
            "confirm_password": "password",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

        # Test missing confirm_password
        form_data = {
            "username": "username",
            "email": "email@example.com",
            "password": "password",
            "confirm_password": "",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_register_form_invalid_email(self):
        """Test that form is invalid with an incorrectly formatted email."""
        form_data = {
            "username": "username",
            "email": "invalid-email",  # Invalid email format
            "password": "password",
            "confirm_password": "password",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_register_form_password_fields_max_length(self):
        """Test that form is invalid if the password fields exceed maximum length."""
        
        # invalid length password field
        form_data = {
            "username": "username",  
            "email": "email@example.com",
            "password": "p" * 41,   #41 characters, exceeding max_length of 40
            "confirm_password": "password",
        }
        
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        
        self.assertEqual(
            form.errors['password'],
            ['Ensure this value has at most 40 characters (it has 41).']
        )
        
        # invalid length confirm password field
        form_data = {
            "username": "username" * 31,  
            "email": "email@example.com",
            "password": "password",   
            "confirm_password": "p" * 41, #41 characters, exceeding max_length of 40
        }
        
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)
        
        self.assertEqual(
            form.errors['confirm_password'],
            ['Ensure this value has at most 40 characters (it has 41).']
        )
    
    def test_register_form_username_max_length(self):
        """Test that form is invalid if the username exceeds maximum length."""
        
        # invalid length username field
        form_data = {
            "username": "u" * 21,   #21 characters, exceeding max_length of 20
            "email": "email@example.com",
            "password": "password",  
            "confirm_password": "password",
        }
        
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
        self.assertEqual(
            form.errors['username'],
            ['Ensure this value has at most 20 characters (it has 21).']
        )
    
    def test_register_form_email_max_length(self):
        """Test that form is invalid if the email exceeds maximum length."""
        
        # invalid length email max
        long_email = "a" * 40 + "@example.com"
        form_data = {
            "username": "usename",
            "email": long_email,    # 40characters, exceeding max_length of 53
            "password": "password",  
            "confirm_password": "password",
        }
        
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
        self.assertEqual(
            form.errors['email'],
            ['Ensure this value has at most 40 characters (it has 52).']
        )
    
    def test_show_password_checked(self):
        """Test if when show password is toggled"""
        
        form_data = {
            "username": "usename",
            "email": "user@example.com",    
            "password": "password",  
            "confirm_password": "password",
            "show_password": True,  # when the show box is checked
        }
        
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
     
    def test_show_password_un_checked(self):
        """Test if when show password is toggled"""
        
        form_data = {
            "username": "usename",
            "email": "user@example.com",    
            "password": "password",  
            "confirm_password": "password",
            "show_password": False,  # when the show box is unchecked
        }
        
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        
    def test_register_form_mismatch_password(self):
        """
        Test that the form is invalid when password and confirm_password do not match.

        Verifies that an error message is shown for the `confirm_password` field when
        the provided `confirm_password` differs from the `password` field.
        """
        
        form_data = {
            "username": "usename",
            "email": "user@example.com",    
            "password": "password",  
            "confirm_password": "password_doesn't_match",
            "show_password": False,  
        }
        
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("confirm_password", form.errors)
        
        self.assertEqual(form.errors['confirm_password'], ["The password doesn't match"])
    