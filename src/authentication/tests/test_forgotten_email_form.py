from django.test import TestCase

from authentication.forms.passwords.forgotten_password import ForgottenPasswordForm


class ForgottenPasswordFormTest(TestCase):
    
    def setUp(self) -> None:
        
        self.form_data = {
            "email": "test_email@example.com"
        }
        
    def test_forgotten_password_form_valid_data(self):
        """Test forgotten password form when form data is valid"""
        
        form = ForgottenPasswordForm(data=self.form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_forgotten_password_form(self):
        """Test forgotten password form when form data is valid"""
        form_data = {
            
        }
        form = ForgottenPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_invalid_email(self):
        """Test forgotten password form when form the email is invalid"""
        
        form_data = {
            "email": "invalid_email"
        }
        form = ForgottenPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'],
            ['Enter a valid email address.']
        )
    
    def test_forgotten_password_form_valid_data(self):
        """Test if it exceeds the maximum length"""
        MAXIMUM_LENGTH = 60
        email          = "e" * MAXIMUM_LENGTH + "@gmail.com"
        
        form_data = {
            "email": email,
        }
        
        form = ForgottenPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        self.assertEqual(
            form.errors['email'],
            ['Ensure this value has at most 60 characters (it has 70).']
        )
    
    def test_email_with_leading_trailing_spaces(self): 
        """test the email when it has trailing spaces"""
        
        form_data = {
        "email": "   test_email@example.com   "
        }
        form = ForgottenPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_email_case_insensitivity(self):
        """test email that case insensitive"""
        
        form_data = {
            "email": "TEST_EMAIL@EXAMPLE.COM"
        }
        form = ForgottenPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())
