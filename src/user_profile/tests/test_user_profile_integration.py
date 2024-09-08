from django.test import TestCase
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile, ShippingAddress, BillingAddress

from utils.country_parser import parse_country_file


class UserProfileIntegrationTests(TestCase):
    
    def setUp(self) -> None:
        self.User         = get_user_model()
        self.username     = "user"
        self.email        = "egbie@example.com"
        self.password     = "password"
        self.user         = self.User.objects.create_user(username=self.username, 
                                                          email=self.email, 
                                                          password=self.password
                                                          )
        self.user_profile = UserProfile.objects.get(user=self.user)
    
        self.COUNTRIES_CHOICES  = parse_country_file("data/countries.txt")
    
    def test_count_of_shipping_addresses_for_user_profile_method(self):
        """Verify that the num_of_shipping_addresses method accurately returns the count of shipping 
            addresses linked to a UserProfile.
        """
        
        # Verify the count when no shipping addresses have been added
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 0)
        
        # Create a shipping address and link it to the user profile
        random_country = self.COUNTRIES_CHOICES[2]
        ShippingAddress.objects.create(country=random_country,
                                       address_1="121 made up street",
                                       city="London",
                                       postcode="r5 211",
                                       user_profile=self.user_profile
                                       )
        
        # Verify the count after adding one address
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 1)
        
        # Add another shipping address and verify the count again
        random_country = self.COUNTRIES_CHOICES[2]
        ShippingAddress.objects.create(country=random_country,
                                       address_1="121A super made up street",
                                       city="London",
                                       postcode="r5 244",
                                       user_profile=self.user_profile
                                       )
      
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 2)
        
        # verify the billing address is 0 and it is not accidently increased when the shipping address is added
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 0)
    
    
    def test_count_of_billing_addresses_for_user_profile_method(self):
        """Verify that the num_of_billing_addresses method accurately returns the count of shipping 
            addresses linked to a UserProfile.
        """
        
        # Verify the count when no billing addresses have been added
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 0)
        
        # Create a shipping address and link it to the user profile
        random_country = self.COUNTRIES_CHOICES[2]
        BillingAddress.objects.create(country=random_country,
                                       address_1="121 made up street",
                                       city="London",
                                       postcode="r5 211",
                                       user_profile=self.user_profile
                                       )
        
        # Verify the count after adding one address
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 1)
        
        # Add another billing and address and verify the count again
        random_country = self.COUNTRIES_CHOICES[2]
        BillingAddress.objects.create(country=random_country,
                                       address_1="121A super made up street",
                                       city="London",
                                       postcode="r5 244",
                                       user_profile=self.user_profile
                                       )
    
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 2)
        
        # verify the shipping address is 0 and it is not accidently increased when the billing address is added
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 0)
    
    
    def test_address_counts_for_user_profile(self):
        """Ensure that the number of billing and shipping addresses linked to the UserProfile 
            are correctly counted and updated when addresses are added.
        """

        # Verify the count when no billing and shipping addresses have been added
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 0)
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 0)
        
        # Add a billing address and link it to the user profile
        random_country = self.COUNTRIES_CHOICES[2]
        BillingAddress.objects.create(country=random_country,
                                       address_1="121 made up street",
                                       city="London",
                                       postcode="r5 211",
                                       user_profile=self.user_profile
                                       )
        
        
        
        # Add a shipping address and link it to the user profile
        random_country = self.COUNTRIES_CHOICES[1]
        ShippingAddress.objects.create(country=random_country,
                                       address_1="121A super made up street",
                                       city="London",
                                       postcode="r5 244",
                                       user_profile=self.user_profile
                                       )
        
        
        # Verify the count when billing and shipping addresses have been added
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 1)
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 1)
       

    def test_shipping_address_count_update_on_deletion(self):
        """Verify that the shipping address count on a user profile is correctly updated when a shipping address
            belonging to the user is deleted.
        """
        
        # Verify the count when no shipping addresses have been added
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 0)
        
        # Add a shipping address and link it to the user profile
        random_country = self.COUNTRIES_CHOICES[1]
        ShippingAddress.objects.create(country=random_country,
                                    address_1="121A super made up street",
                                    city="London",
                                    postcode="r5 244",
                                    user_profile=self.user_profile
                                    )
        
        # Verify that the shipping address count is now 1 after adding a shipping address
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 1)
                
        # Get the shipping address belonging to the user profile
        shipping_address = ShippingAddress.objects.filter(country=random_country).first()
        self.assertIsNotNone(shipping_address)
        
        shipping_address.delete()
        
        # Verify that the shipping address count is back to 0 after deletion
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 0)

    def test_billing_address_count_update_on_deletion(self):
        """Verify that the billing address count on a user profile is correctly updated when a billing address
            belonging to the user is deleted.
        """
        
        # Verify the count when no shipping addresses have been added
        self.assertEqual(self.user_profile.num_of_shipping_addresses(), 0)
        
        # Add a shipping address and link it to the user profile
        random_country = self.COUNTRIES_CHOICES[1]
        BillingAddress.objects.create(country=random_country,
                                    address_1="121A super made up street",
                                    city="London",
                                    postcode="r5 244",
                                    user_profile=self.user_profile
                                    )
        
        # Verify that the billing address count is now 1 after adding a shipping address
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 1)
                
        # Get the billing address belonging to the user profile
        billing_address = BillingAddress.objects.filter(country=random_country).first()
        self.assertIsNotNone(billing_address)
        

        # Verify that the billing address count is back to 0 after deletion
        self.assertEqual(self.user_profile.num_of_billing_addresses(), 0)

    def tearDown(self) -> None:
        """Clean up the database after each test."""
        ShippingAddress.objects.all().delete()
        UserProfile.objects.all().delete()
        self.User.objects.all().delete()
