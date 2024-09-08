from django.test import TestCase
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile, ShippingAddress, BillingAddress

from utils.country_parser import parse_country_file


def set_up_user_profile():
     User     = get_user_model()
     user     = User.objects.create_user(username="user", 
                                        email="egbie@example.com", 
                                        password="password",
                                        )
     user_profile = UserProfile.objects.get(user=user)
     return user_profile


class BillingAddressTests(TestCase):
    
    def setUp(self):
        self.COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")
        self.RANDOM_COUNTRY     = self.COUNTRIES_CHOICES[0]
        self.ADDRESS_1          = "121 Random address"
        self.ADDRESS_2          = "Random street name"
        self.CITY               = "London"
        self.POSTCODE           = "E9, 145"
        self.user_profile       = set_up_user_profile()
        self.COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")
        
        self.billing_address = BillingAddress.objects.create(country=self.RANDOM_COUNTRY,
                                                             address_1=self.ADDRESS_1,
                                                             address_2=self.ADDRESS_2,
                                                             city=self.CITY,
                                                             postcode=self.POSTCODE,
                                                             user_profile=self.user_profile, 
                                                             )

    def test_creation_count(self):
        """Test that the number of creation count is successfully created"""
        
        num_of_billing_address = BillingAddress.objects.count()
        self.assertEqual(num_of_billing_address, 1)
    
    def test_billing_attributes_fields_are_correct(self):
        """Test if the billing address fields match"""
        
        # Retrieve the object from the database to verify it was successfully created and stored
        billing_address = BillingAddress.objects.first()
        
        self.assertEqual(str(billing_address.country), str(self.RANDOM_COUNTRY))
        self.assertEqual(billing_address.address_1, self.ADDRESS_1)
        self.assertEqual(billing_address.address_2, self.ADDRESS_2)
        self.assertEqual(billing_address.city, self.CITY)
        self.assertEqual(billing_address.postcode, self.POSTCODE)
        self.assertEqual(billing_address.user_profile, self.user_profile)
    
    def test_if_billing_address_is_not_marked_primary_address(self):
        """Ensure that a newly created billing address is not automatically marked as the primary address 
        for the user profile unless explicitly set."""
        self.assertFalse(self.billing_address.primary_address)
        
    def test_billing_address_can_be_marked_as_primary(self):
        """
        Test that the billing address can be marked as the primary address 
        for a UserProfile.
        """
        # check that primary address is marked as false
        self.assertFalse(self.billing_address.primary_address)
        
        self.billing_address.mark_as_primary()
       
        # get the billing address from db
        billing_address = BillingAddress.objects.first()
        
        self.assertTrue(billing_address.primary_address)
        
        
    def test_billing_address_can_be_unmarked_as_primary(self):
        """
        Test that the billing address can be marked as the primary address 
        for a UserProfile.
        """
        # Mark the primary address as primary
        self.billing_address.mark_as_primary()
        billing_address = BillingAddress.objects.first()
        
        self.assertTrue(billing_address.primary_address)
        
        # mark the address as not primary
        self.billing_address.unmark_as_primary()
       
        # get the billing address from db
        billing_address = BillingAddress.objects.first()
        
        self.assertFalse(billing_address.primary_address)
        
       

class ShippngAddressTests(TestCase):
    
    def setUp(self):
        self.COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")
        self.RANDOM_COUNTRY     = self.COUNTRIES_CHOICES[0]
        self.ADDRESS_1          = "121 Random address"
        self.ADDRESS_2          = "Random street name"
        self.CITY               = "London"
        self.POSTCODE           = "E9, 145"
        self.user_profile       = set_up_user_profile()
        self.COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")
        
        self.shipping_address = ShippingAddress.objects.create(country=self.RANDOM_COUNTRY,
                                                             address_1=self.ADDRESS_1,
                                                             address_2=self.ADDRESS_2,
                                                             city=self.CITY,
                                                             postcode=self.POSTCODE,
                                                             user_profile=self.user_profile, 
                                                             )

    def test_creation_count(self):
        """Test that the number of creation count is successfully created"""
        
        num_of_shipping_address = ShippingAddress.objects.count()
        self.assertEqual(num_of_shipping_address, 1)
    
    def test_shipping_attributes_fields_are_correct(self):
        """Test if the shipping address fields match"""
        
        # Retrieve the object from the database to verify it was successfully created and stored
        shipping_address = ShippingAddress.objects.first()
        
        self.assertEqual(str(shipping_address.country), str(self.RANDOM_COUNTRY))
        self.assertEqual(shipping_address.address_1, self.ADDRESS_1)
        self.assertEqual(shipping_address.address_2, self.ADDRESS_2)
        self.assertEqual(shipping_address.city, self.CITY)
        self.assertEqual(shipping_address.postcode, self.POSTCODE)
        self.assertEqual(shipping_address.user_profile, self.user_profile)
    
 
  
        
   
