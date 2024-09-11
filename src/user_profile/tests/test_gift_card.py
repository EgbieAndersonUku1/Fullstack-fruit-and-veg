from datetime import datetime
from decimal import Decimal, getcontext
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from user_profile.models import GiftCard, UserProfile
from .user_profile_set_up import set_up_user_profile
from utils.generator import generate_token
from utils.converter import string_to_date



class GiftCardTest(TestCase):
    
    def setUp(self):
        
        self.REWARD_CARD_TYPE = "Reward card"
        self.VALID_TOKEN            = generate_token()
        self.EXPIRY_DATE      = "2024-10-09"
        self.VALUE            = 25
    
        self.user_profile = set_up_user_profile()
        
        self.gift_card = GiftCard.objects.create(
            card_type=self.REWARD_CARD_TYPE,
            code=self.VALID_TOKEN,
            expiration_date=self.EXPIRY_DATE,
            user_profile=self.user_profile,
            value=self.VALUE,
        )
    
    def test_created(self):
        """Test if the gift card has successfully being created"""
        
        self.assertEqual(GiftCard.objects.count(), 1)
    
    def test_gift_card_has_correct_attributes_after_creation(self):
        """
        Verify that a BillingAddress object has the correct attributes after being created in the database.

        This test ensures that when a BillingAddress instance is created, its attributes are set correctly and match
        the values provided during creation. It checks that the fields of the BillingAddress object reflect the expected
        values for country, address lines, city, postcode, and associated user profile.
        """
        
        self.assertEqual(self.gift_card.card_type, self.REWARD_CARD_TYPE)
        self.assertEqual(self.gift_card.code, self.VALID_TOKEN)
        self.assertEqual(self.gift_card.expiration_date, self.EXPIRY_DATE)
        self.assertEqual(self.gift_card.value, self.VALUE)
        self.assertEqual(self.gift_card.user_profile, self.user_profile)
        
    def test_gift_card_is_not_created_active(self):
        """
        Verify that the gift card is not created as an active gift card.
        """
        self.assertFalse(self.gift_card.is_active)
    
    def test_gift_card_is_not_already_redeemed(self):
        """
        Verify that the gift card is not already redeemed
        """
        self.assertFalse(self.gift_card.is_redeemed)
    
    def test_date_created_is_not_in_future(self):
        """
        Verify that the date_created field on the gift card is not set to a future date.
        
        This test ensures that when a gift card is created, its date_created attribute reflects a timestamp
        that is less than or equal to the current time, confirming that the date_created is set correctly and
        not inadvertently set to a future date.
        """
        current_time = timezone.now()
        self.assertLessEqual(self.gift_card.date_created, current_time)

    def test_value_created_is_zero(self):
        """
        Verify that the gift card is created with a default value of 0.

        This test ensures that when a gift card is created, its amount is set to 0 by default,
        confirming that the value field is correctly initialized.
        """
        
        self.user_profile = set_up_user_profile(username="user2", email="user2@gmail.com")
        CARD_TYPE         = "Promotion card"
        
        # create gift card
        gift_card = GiftCard.objects.create(
            card_type=CARD_TYPE,
            code=generate_token(),
            expiration_date=self.EXPIRY_DATE,
            user_profile=self.user_profile,
        )
        
        gift_card.refresh_from_db()
        
        self.assertIsNotNone(gift_card)
        self.assertEqual(gift_card.value, 0)
        

    def test_token_is_unique(self):
        """
        Verify that an IntegrityError is raised when attempting to create a gift card
        with a duplicate token.
        """
        
        # Attempt to create a second gift card with the same token
        with self.assertRaises(IntegrityError):
            self.user_profile = set_up_user_profile()
        
            self.gift_card = GiftCard.objects.create(
                card_type=self.REWARD_CARD_TYPE,
                code=self.VALID_TOKEN,
                expiration_date=self.EXPIRY_DATE,
                user_profile=self.user_profile,
                value=self.VALUE,
            )

    def test_card_is_not_created_as_non_expire(self):
        """
        Test that card is not created as a gift card that doens't expire
        """
        self.assertFalse(self.gift_card.does_not_expire)
        
        
    
class GiftCardMethodsTest(TestCase):
    
    def setUp(self):
        
        self.REWARD_CARD_TYPE = "Reward card"
        self.VALID_TOKEN      = generate_token()
        self.EXPIRY_DATE      = "2024-10-09"
        self.VALUE            = 25
        self.ACTIVE           = True
    
        self.user_profile = set_up_user_profile()
        
        self.gift_card = GiftCard.objects.create(
            card_type=self.REWARD_CARD_TYPE,
            code=self.VALID_TOKEN,
            is_active=self.ACTIVE,
            expiration_date=self.EXPIRY_DATE,
            user_profile=self.user_profile,
            value=self.VALUE,
        )
    
    def test__str__method(self):
        """Test if the str method returns the correct string response"""
        
        user_profile = self.gift_card.user_profile
        expected_str = f"Gift card for {user_profile.username.title()} with the amount of £{self.gift_card.value:.2f}"
        
        self.assertEqual(str(self.gift_card), expected_str)
        
    def test_is_valid_method(self):
        """
        Test the is_valid method to ensure it returns the correct boolean value
        based on the gift card's state (active, redeemed, expired, or with an invalid token).
        """

        # Test: Valid token when the card is active
        self.assertTrue(self.gift_card.is_valid(self.VALID_TOKEN))

        # Test: Valid token but the card is inactive
        self.gift_card.is_active = False
        self.gift_card.save()
        self.assertFalse(self.gift_card.is_valid(self.VALID_TOKEN))

        # Test: Valid token but the card has expired
        expired_date                   = "2022-10-06"
        self.gift_card.expiration_date = expired_date
        self.gift_card.is_active       = self.ACTIVE
        self.gift_card.save()
        
        self.gift_card.refresh_from_db()
        self.assertFalse(self.gift_card.is_valid(self.VALID_TOKEN), "The should print that card has exprired")

        # Test: Valid token but the card has been redeemed
        self.gift_card.is_redeemed = True
        
        self.gift_card.save()
        self.gift_card.refresh_from_db()
        self.assertFalse(self.gift_card.is_valid(self.VALID_TOKEN))

        # # Test: Invalid token
        invalid_token                  = generate_token()
        self.gift_card.code            = invalid_token
        self.gift_card.expiration_date = self.EXPIRY_DATE
        self.gift_card.is_redeemed     = False
        self.gift_card.is_active       = self.ACTIVE
        self.gift_card.save()
        self.gift_card.refresh_from_db()
        self.assertFalse(self.gift_card.is_valid(self.VALID_TOKEN))

    def test_apply_method(self):
        """Test if the apply method correctly updates the value amount"""
        
        # create gift card with amount of 30
        user_profile     = set_up_user_profile(username="user4", email="user4@example.com")
        GIFT_CARD_AMOUNT = 30
        
        gift_card = GiftCard.objects.create(
            card_type=self.REWARD_CARD_TYPE,
            code=generate_token(),
            is_active=self.ACTIVE,
            expiration_date=self.EXPIRY_DATE,
            user_profile=user_profile,
            value=GIFT_CARD_AMOUNT,
        )
        
        getcontext().prec = 2
       
        NEW_AMOUNT        = 10
        DEDUCTABLE_AMOUNT = 20
        gift_card.apply(Decimal(DEDUCTABLE_AMOUNT))
        
        self.assertEqual(gift_card.value, Decimal(NEW_AMOUNT))
    
    def test_apply_method_when_amount_is_less_than(self):
        """Test if a ValueError is raised when the amount entered is less than or equal to zero"""
        
        # create gift card with amount of 30
        user_profile     = set_up_user_profile(username="user5", email="user5@example.com")
        GIFT_CARD_AMOUNT = 30
        
        gift_card = GiftCard.objects.create(
            card_type=self.REWARD_CARD_TYPE,
            code=generate_token(),
            is_active=self.ACTIVE,
            expiration_date=self.EXPIRY_DATE,
            user_profile=user_profile,
            value=GIFT_CARD_AMOUNT,
        )
        
        DEDUCTABLE_AMOUNT = 0
        
        with self.assertRaises(ValueError) as context:
            gift_card.apply(Decimal(DEDUCTABLE_AMOUNT))
        
        self.assertEqual(str(context.exception), "The amount must be greater than zero.")
   
    def test_apply_method_when_amount_exceeds_gift_card_balance(self):
        """Test that a ValueError is raised when the amount applied exceeds the gift card's balance."""
        
        # Create gift card with amount of 30
        user_profile     = set_up_user_profile(username="user5", email="user5@example.com")
        GIFT_CARD_AMOUNT = 30
        
        self.gift_card = GiftCard.objects.create(
            card_type=self.REWARD_CARD_TYPE,
            code=generate_token(),
            is_active=self.ACTIVE,
            expiration_date=self.EXPIRY_DATE,
            user_profile=user_profile,
            value=GIFT_CARD_AMOUNT,
        )
        
        DEDUCTABLE_AMOUNT = 40
        
        with self.assertRaises(ValueError) as context:
            self.gift_card.apply(Decimal(DEDUCTABLE_AMOUNT))
        
        self.assertEqual(str(context.exception), "Insufficient balance on the gift card.")

    def test_save_parameter_in_apply_method(self):
        """Test the save parameter in apply method"""
        
        DEDUCTABLE_AMOUNT = 10
        EXPECTED_AMOUNT   = 15
        
        # test if the value is equal to the original amount
        self.assertEqual(self.gift_card.value, self.VALUE)
        
        self.gift_card.apply(Decimal(DEDUCTABLE_AMOUNT))   # automatic save
        
        self.gift_card.refresh_from_db() 
        self.assertEqual(self.gift_card.value, EXPECTED_AMOUNT)
        
        # disable save
        self.gift_card.apply(Decimal(DEDUCTABLE_AMOUNT), save=False)
        self.gift_card.refresh_from_db() 
        self.assertEqual(self.gift_card.value, EXPECTED_AMOUNT)
    
    def test_deactivate_saves_correctly(self):
        """Test that deactivating the gift card saves the change to the database."""
        
        self.assertTrue(self.gift_card.is_active, "The card should be active")
        
        # Deactivate the card
        self.gift_card.deactivate(save=True)
        self.gift_card.refresh_from_db()  
        
        self.assertFalse(self.gift_card.is_active, "The gift card should be inactive after deactivation.")

    def test_activate_saves_correctly(self):
        """Test that activating the gift card saves the change to the database."""
    
        self.assertTrue(self.gift_card.is_active)
        self.gift_card.deactivate(save=True)
        
        # Now activate the card
        self.gift_card.activate(save=True)
        self.gift_card.refresh_from_db()           

        # Assert that the card is activated
        self.assertTrue(self.gift_card.is_active, "The gift card should be active after activation.")
     
    def test_activate_method(self):
        """Test the activate method of the GiftCard model."""

        # Deactivate the card and verify the change
        self.gift_card.deactivate()
        self.gift_card.save()  
        self.gift_card.refresh_from_db()
        self.assertFalse(self.gift_card.is_active, "The gift card should be inactive after deactivation.")

        # Activate the card and verify the change
        self.gift_card.activate()
        self.gift_card.save() 
        self.gift_card.refresh_from_db()
        self.assertTrue(self.gift_card.is_active, "The gift card should be active after activation.")

    def test_issue_gift_card(self):
        """Test if a new gift card can be issued"""
        
        CARD_TYPE        = "test card"
        CARD_EXPIRY_DATE = "2105-09-01"
        CARD_VALUE       = Decimal("5")
        new_user_profile = set_up_user_profile(username="new user", 
                                            email="new_user@gmail.com", 
                                            password="password1"
                                            )
        
        GiftCard.issue_gift_card(card_type=CARD_TYPE,
                                 amount=CARD_VALUE,
                                 expiry_date=CARD_EXPIRY_DATE,
                                 user=new_user_profile,
                                 )
        
        # check if it is in db
        new_issue_gift_card = GiftCard.objects.filter(card_type=CARD_TYPE)
        self.assertTrue(new_issue_gift_card.exists())
        
        # check if fields match
        new_issue_gift_card = new_issue_gift_card.first()
        
        expire_date  = string_to_date(CARD_EXPIRY_DATE)
        self.assertEqual(new_issue_gift_card.card_type, CARD_TYPE)
        self.assertEqual(new_issue_gift_card.value, CARD_VALUE),
        self.assertEqual(new_issue_gift_card.expiration_date, expire_date)
        self.assertEqual(new_issue_gift_card.user_profile, new_user_profile)
        self.assertFalse(new_issue_gift_card.does_not_expire)
    
    def test_issue_gift_card_that_does_not_expire(self):
        """Issue a gift card that doesn't expire"""
        
        CARD_TYPE        = "does not expire card"
        CARD_EXPIRY_DATE = "2095-09-01"
        CARD_VALUE       = Decimal("5")
        new_user_profile = set_up_user_profile(username="new user", 
                                            email="new_user@gmail.com", 
                                            password="password1"
                                            )
        
        GiftCard.issue_gift_card(card_type=CARD_TYPE,
                                 amount=CARD_VALUE,
                                 expiry_date=CARD_EXPIRY_DATE,
                                 user=new_user_profile,
                                 does_not_expire=True
                                 )
        
        non_expiring_gift_card = GiftCard.objects.filter(card_type=CARD_TYPE).first()
        
        self.assertTrue(non_expiring_gift_card.does_not_expire)
        
        # Ensure the expiration date is null when does_not_expire is set.
        # Even if a date value is provided, it should automatically be null.
        self.assertIsNone(non_expiring_gift_card.expiration_date)
        
        
    def test_set_expiry_date_method(self):
        """Test if the expiry date can be set"""
        
        CARD_EXPIRY_DATE = string_to_date("2029-01-01")
       
        # assert that the current expiry date is not equally to expiry date to be set
        self.assertNotEqual(self.gift_card.expiration_date, CARD_EXPIRY_DATE)
        
        # set the expiry date
        self.gift_card.set_expiry_date(CARD_EXPIRY_DATE)
        self.gift_card.refresh_from_db()
        
        # check that the saved date equals the date used in the set_expiry_date
        self.assertEqual(self.gift_card.expiration_date, CARD_EXPIRY_DATE)
    
    def test_set_expiry_date_does_not_expire_flag(self):
        """
        Test that the `does_not_expire` flag can be set using the `set_expiry_date` method.
        """
        
        # set does not expire flag to false
        self.gift_card.does_not_expire = False
        self.gift_card.save()
        self.gift_card.refresh_from_db()
        
        self.assertFalse(self.gift_card.does_not_expire, "This gift `does_not_expire` should be set to False")
        
        # save using the `set_expriy_date` method
        self.gift_card.set_expiry_date(does_not_expire=True)
        self.gift_card.refresh_from_db()
        
        self.assertTrue(self.gift_card.does_not_expire, "This gift `does_not_expire` should be set to True")
      
    def tearDown(self) -> None:
        """Clean up the database by deleting all test data after every test"""
        GiftCard.objects.all().delete()
        User = get_user_model()
        User.objects.all().delete()
        UserProfile.objects.all().delete()
