from django.test import TestCase
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile, ShippingAddress, BillingAddress

from utils.country_parser import parse_country_file
from .user_profile_set_up import set_up_user_profile



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
        
    def test_that_only_one_address_is_marked_as_primary(self):
        """
        Test that only one billing address is marked as primary for a given user profile, and ensure that 
        marking a new address as primary unmarks the previous one. Also verify that other user profiles
        are not affected by this change.
        """
        
        # Create three new user profiles
        user_profile_1 = set_up_user_profile(username="user1", email="user@example.com", password="password1")
        user_profile_2 = set_up_user_profile(username="user2", email="user2@example.com", password="password2")
        user_profile_3 = set_up_user_profile(username="user3", email="user3@example.com", password="password3")
        
        
        # Create a billing address for each user profile
        self.billing_address_1 = BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY, address_1=self.ADDRESS_1, address_2=self.ADDRESS_2,
            city=self.CITY, postcode=self.POSTCODE, user_profile=user_profile_1)
        
        self.billing_address_2 = BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY, address_1=self.ADDRESS_1, address_2=self.ADDRESS_2,
            city=self.CITY, postcode=self.POSTCODE, user_profile=user_profile_2)
        
        self.billing_address_3 = BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY, address_1=self.ADDRESS_1, address_2=self.ADDRESS_2,
            city=self.CITY, postcode=self.POSTCODE, user_profile=user_profile_3)
    
        # Create three more billing addresses for user_profile_1 and mark them all as primary addresses
        BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY, address_1="121A Thor rules", address_2="Crossway groves",
            city="London", postcode="E5 u1", user_profile=user_profile_1, primary_address=True)
        
        BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY, address_1="131 Black widow rules", address_2="Crossway groves",
            city="London", postcode="E5 u2", user_profile=user_profile_1, primary_address=True)
        
        BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY, address_1="131 Stranger Things rules", address_2="Crossway groves", 
            city="London", postcode="E5 u3", user_profile=user_profile_1, primary_address=True)
        
        # Verify that only the last billing address is marked as primary, and the previous ones are unmarked
        billing_address_1 = BillingAddress.objects.filter(postcode="E5 u1").first()
        billing_address_2 = BillingAddress.objects.filter(postcode="E5 u2").first()
        billing_address_3 = BillingAddress.objects.filter(postcode="E5 u3").first()
        
        self.assertFalse(billing_address_1.primary_address)
        self.assertFalse(billing_address_2.primary_address)
        self.assertTrue(billing_address_3.primary_address)
        
        # Verify that other user profiles have not been marked as primary addresses
        billing_address_profile_2 = BillingAddress.objects.filter(user_profile=user_profile_2, primary_address=True).all()
        billing_address_profile_3 = BillingAddress.objects.filter(user_profile=user_profile_3, primary_address=True).all()
        
        self.assertFalse(billing_address_profile_2.exists())
        self.assertFalse(billing_address_profile_3.exists())


    def test_no_primary_address_set(self):
        """
        Test that no billing address is marked as primary when none is explicitly set.
        The system should allow multiple addresses without requiring a primary one.
        """
        user_profile = set_up_user_profile(username="user_profile6", email="user_profile6@example.com", password="password6")
        
        CITY = "Sin City"
        
        # Create a billing address without marking it as primary
        BillingAddress.objects.create(
            country=self.RANDOM_COUNTRY,
            address_1=self.ADDRESS_1,
            address_2=self.ADDRESS_2,
            city=CITY,
            postcode=self.POSTCODE,
            user_profile=user_profile
        )
        
        address = BillingAddress.objects.filter(city=CITY).first()
        
        # Ensure the address is created and belongs to the user_profile
        self.assertIsNotNone(address)
        self.assertEqual(address.user_profile, user_profile)
        
        # Ensure the address is not marked as primary
        self.assertFalse(address.primary_address)

        
        
        
        
        
        
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
 
   
