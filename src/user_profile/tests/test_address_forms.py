from django.test import TestCase


from user_profile.forms.user_profile_form import BillingAddressForm, ShippingAddressForm

from utils.country_parser import parse_country_file

COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")

class PrimaryAddress:
    YES = '1'
    NO  = '2'
    CHOICES = [(YES, 'Yes'), (NO, 'No')]

class AddressFormTests(TestCase):
    
    def setUp(self):
        # Setup sample data for the forms
        self.form_data = {
            'country': COUNTRIES_CHOICES[0][0],  
            'address_1': '123 Main St',
            'address_2': 'Apt 4B',
            'city': 'Somewhere',
            'state': 'CA',
            'postcode': '90001',
            'is_primary_address': PrimaryAddress.YES  
        }
    
                
    def test_billing_address_form_valid_with_correct_data(self):
        """Test that the BillingAddressForm is valid with correct data."""
        form = BillingAddressForm(data=self.form_data)
     
        self.assertTrue(form.is_valid(), f"Form should be valid: {form.errors}")
        self.assertEqual(form.cleaned_data['is_primary_address'], PrimaryAddress.YES)

    def test_shipping_address_form_valid_with_correct_data(self):
        """Test that the ShippingAddressForm is valid with correct data."""
        
        form = ShippingAddressForm(data=self.form_data)
        self.assertTrue(form.is_valid(), f"Form should be valid: {form.errors}")

    def test_multiple_forms_can_be_submitted_together(self):
        """Test if multiple forms can be submitted together successfully."""
        
        billing_form = BillingAddressForm(data=self.form_data)
        shipping_form = ShippingAddressForm(data=self.form_data)
        
      
        if billing_form.is_valid() and shipping_form.is_valid():
           
            billing_address  = billing_form.save(commit=False)
            shipping_address = shipping_form.save(commit=False)
            
            # Assertions to ensure forms create the expected objects
            self.assertIsNotNone(billing_address, "Billing address should not be None")
            self.assertIsNotNone(shipping_address, "Shipping address should not be None")
            
        else:
            print("Forms are not valid:")
            print("Billing Form Errors:", billing_form.errors)
            print("Billing Form Cleaned Data:", billing_form.cleaned_data if billing_form.is_valid() else "N/A")
            print("Shipping Form Errors:", shipping_form.errors)
            print("Shipping Form Cleaned Data:", shipping_form.cleaned_data if shipping_form.is_valid() else "N/A")
          
            self.fail("Both forms should be valid but are not.")
