from django.test import TestCase
from django import forms

from authentication.forms.passwords.new_password import NewPasswordForm


class NewPasswordFormTest(TestCase):
    
    def setUp(self):
        self.form_data = {
            "new_password": "Pa$$word1",
            "confirm_password": "Pa$$word1",
        }
        
    def test_new_password_form_valid_data(self):
    
        form = NewPasswordForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_new_password_form_empty_data(self):
        
        invalid_data = {
            "new_password": "",
            "confirm_password": ""
        }
        
        form = NewPasswordForm(data=invalid_data)
        self.assertFalse(form.is_valid())
    
    def test_new_password_form_when_new_password_is_empty(self):
        invalid_data = {
            "new_password": "",
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_password"], ['This field is required.'])

    def test_new_password_form_when_confirm_password_is_empty(self):
        invalid_data = {
            "new_password": "Pa$$word1",
            "confirm_password": ""
        }
        
        form = NewPasswordForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["confirm_password"], ['This field is required.'])
        
    def test_clean_new_password_raises_validation_error_with_incorrect_length(self):
        
        form_data = {
            "new_password": "P", # to short
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least eight characters"])
        
    
    def test_new_password_raises_validation_error_with_incorrect_length(self):
        
        form_data = {
            "new_password": "P", # to short
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least eight characters"])
    
    def test_new_password_raises_validation_error_with_missing_numbers(self):
        
        form_data = {
            "new_password": "Password", # missing numbers
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least one number"])
    
    def test_new_password_raises_validation_error_with_no_lowercases(self):
        
        form_data = {
            "new_password": "PA2SSWORD", # no lowercases
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least one lowercase"])
    
    def test_new_password_raises_validation_error_with_no_lowercases(self):
        
        form_data = {
            "new_password": "pass2word", # no uppercases
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least one uppercase"])
        
    
    def test_new_password_raises_validation_error_with_no_uppercases(self):
        
        form_data = {
            "new_password": "pass2word", # no uppercases
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least one uppercase"])
    
    
    def test_new_password_raises_validation_error_with_no_special_characters(self):
        
        form_data = {
            "new_password": "pass2Word", # no special characters
            "confirm_password": "Pa$$word1"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors)
        
        self.assertEqual(form.errors["new_password"], ["The password must contain at least one special character"])
        
    
    def test_mismatch_password(self):
        
        form_data = {
            "new_password": "Pa$$word1", 
            "confirm_password": "Pa$$word2"
        }
        
        form = NewPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        
          # Check if the 'non_field_errors' has the expected error
        self.assertIn("The passwords does not match", form.non_field_errors())
        
       