from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, DataError
from random import randint
from django.core.files.uploadedfile import SimpleUploadedFile
from uuid import uuid4

from product.models import Brand, ProductVariation, Product, Category, Manufacturer
from product.tests.factory import ProductFactory, BrandFactory, ManufacturerFactory, CategoryFactory

from factory import Faker

# Create your tests here.
class ProductModelTest(TestCase):
    
    def setUp(self):
        self.related_fields =  {
            "name": "Test name",
            "long_description": "Test description",
            "short_description": "Short description",
            "sku": "sku",
            "upc": "upc",
            "brand": BrandFactory(),
            "category": CategoryFactory(),
            "manufacturer": ManufacturerFactory(),
            "weight": randint(1, 50),
            "primary_image": SimpleUploadedFile("primary_image.jpg", b"file_content", content_type="image/jpeg"),
            "side_image": SimpleUploadedFile("side_image.jpg", b"file_content", content_type="image/jpeg"),
            "side_image_2": SimpleUploadedFile("side_image_2.jpg", b"file_content", content_type="image/jpeg"),
            "country_of_origin": Faker("country"),
        }
        
    def test_single_product_creation(self):
        """Test if a single product has been created and saved in the database"""
        
        ProductFactory()

        EXPECTED_COUNT = 1
        
        self.assertEqual(Product.objects.count(), EXPECTED_COUNT)
        
    def test_product_factory_creates_product_with_default_values(self):
        """Test that the ProductFactory creates a Product with default values"""
        
        product = ProductFactory()
        
        self.assertIsInstance(product, Product)
        self.assertFalse(product.is_featured)
        self.assertTrue(product.name)
        self.assertGreater(product.price, 0)
        self.assertGreater(product.weight, 0)
        self.assertIsNotNone(product.primary_image)
        self.assertIsNotNone(product.side_image)
        self.assertIsNotNone(product.side_image_2)
        self.assertIsInstance(product.brand, Brand)
        self.assertIsInstance(product.category, Category)
        self.assertIsInstance(product.manufacturer, Manufacturer)

    def test_product_name_is_saved_correctly(self):
        """Test if a product's custom name is saved correctly to the database"""

        product = ProductFactory()
        
        # Test if it was saved to the database
        product_in_db = Product.objects.filter(name=product.name).exists()
        self.assertTrue(product_in_db)

    def test_name_does_not_save_exceed_length(self):
        """Test that the name doesn't save when it exceeds the expected length"""
        
        # Dynamically fetch the max length from the model field
        expected_character_length = Product._meta.get_field('name').max_length
        
        # Generate a string that exceeds the limit
        long_name        = "l" * (expected_character_length + 1)
        long_name_length = len(long_name)
        exceeds_by       = long_name_length - expected_character_length
        
        with self.assertRaises(DataError, msg=(
            f"Long name exceeds the expected length of {expected_character_length} characters. "
            f"Current Length: {long_name_length} -- exceeds by {exceeds_by}."
        )):
            _ = ProductFactory(name=long_name)

    def test_long_description_is_saved_correctly(self):
        """Test if a product description is saved in the database"""
        
        product       = ProductFactory()
        saved_product = Product.objects.get(id=product.id)
        
        # Test if it was saved to the database
        self.assertEqual(product.long_description, saved_product.long_description)

    def test_short_description_does_not_save_when_description_exceed_expected_length(self):
        """Test that short description raises an error when it exceeds the expected length."""
        
        # Dynamically fetch the max length from the model field
        expected_character_length = Product._meta.get_field('short_description').max_length
        
        # Generate a string that exceeds the limit
        long_short_description = "l" * (expected_character_length + 1)
        description_length     = len(long_short_description)
        exceeds_by             = description_length - expected_character_length
        
        with self.assertRaises(ValidationError, msg=(
            f"Short description exceeds the expected length of {expected_character_length} characters. "
            f"Current Length: {description_length} exceeds by {exceeds_by}."
        )):
            ProductFactory(short_description=long_short_description)

    def test_is_featured_is_automatically_created_as_false_and_saved(self):
        """Test if 'is_featured' defaults to False and the product is saved to the database."""
        
        product = ProductFactory()
        
        # Assert the product instance is saved in the database is false
        product_in_db = Product.objects.get(id=product.id)
        self.assertFalse(product_in_db.is_featured)
    
    def test_if_sku_is_automatically_created_by_default(self):
        """Test if the SKU is automatically created by defalut"""
        
        product = ProductFactory()
        
        saved_in_db = Product.objects.get(id=product.id)
        self.assertIsNotNone(saved_in_db.sku)
        self.assertEqual(product.sku, saved_in_db.sku)

    def test_if_sku_can_be_added_by_user(self):
        """Test if a user-defined SKU can be added and saved in the database."""
        
        sku     = "TEST-SKU-123"
        product = ProductFactory(sku=sku)
        
        # Check if the product SKU is set correctly
        self.assertEqual(product.sku, sku, "The SKU should match the user-defined token.")
        
        # Check if the product with the specified SKU exists in the database
        product_exists = Product.objects.filter(sku=sku).exists()
        self.assertTrue(product_exists, "The product with the specified SKU should exist in the database.")
        
    def test_database_enforces_unique_sku(self):
        """Ensure the database raises an IntegrityError for duplicate SKUs."""
        
        sku     = "TEST-SKU-123"
        ProductFactory(sku=sku)
        
        # Attempt to create another product with the same SKU, which should fail
        with self.assertRaises(IntegrityError, msg="Expected an IntegrityError when trying to create a product with a duplicate SKU"):
            ProductFactory(sku=sku)

    def test_database_enforces_unique_upc(self):
        """Ensure the database raises an IntegrityError for duplicate SKUs."""
        
        upc     = "TEST-UPC-123"
        ProductFactory(upc=upc)
        
        # Attempt to create another product with the same UPC, which should fail
        with self.assertRaises(IntegrityError, msg="Expected an IntegrityError when trying to create a product with a duplicate UPC"):
            ProductFactory(upc=upc)
            
    def test_price_is_saved_correctly(self):
        """Test if the price is saved correctly"""
        
        product = ProductFactory()
        
        product_exists = Product.objects.filter(price=product.price).exists()
        self.assertIsNotNone(product_exists)
        
    def test_price_exceeding_maximum_digits_raises_error(self):
        """Ensure a ValidationError is raised when the price exceeds the maximum allowed digits."""

        # Dynamically fetch the max digits allowed for the price field
        max_digits     = Product._meta.get_field('price').max_digits
        invalid_price  = 10 ** (max_digits + 1)  # e.g., max_digits = 10 -> invalid_price = 10000000000
        
        with self.assertRaises(DataError, msg=f"Expected ValidationError when attempting to save a price exceeding {max_digits} digits."):
            ProductFactory(price=invalid_price)
    
    def test_price_exceeding_maximum_decimal_places_raises_error(self):
        """Ensure a ValidationError is raised when the price exceeds the allowed decimal places."""
        
        # Dynamically fetch the max decimal places allowed for the price field
        max_decimal_places = Product._meta.get_field('price').decimal_places
        
        # Create an invalid price that exceeds the allowed decimal places
        price = 250.5568822544
        invalid_price = round(price, max_decimal_places + 1)  # Adding 1 extra decimal place amd round to specified decimal e.g 3, 4, etc

        with self.assertRaises(ValidationError, msg=f"Expected a ValidationError as the price exceeds {max_decimal_places} decimal places."):
             # use Product model since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.price = invalid_price
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()

    def test_negative_price_raises_error(self):
        """Ensure a ValidationError is raised when the price entered is negative."""
        
        invalid_price = -1

        with self.assertRaises(ValidationError, msg=("Expected an error message to be raised because the price entered is negative")):
            # use Product model since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.price = invalid_price
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()

    def test_error_when_discount_price_none_and_is_discounted_true(self):
        """Ensure a ValidationError is raised when is_discounted_price is True but discount_price is None."""
        
        with self.assertRaises(ValidationError, 
                                msg="Expected a ValidationError because discount price is None while is_discounted_price is True"
                                ):
            # Use Product model directly since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.is_discounted_price = True
            product.discount_price      =  None
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()

    def test_error_when_discount_price_is_set_and_is_discounted_false(self):
        """Ensure a ValidationError is raised when is_discounted_price is False but discount_price is set"""
        
        with self.assertRaises(ValidationError, 
                                msg="Expected a ValidationError because discount price is set but is_discounted_price is set to false"
                                ):
            # Use Product model directly since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.is_discounted_price = False
            product.discount_price      = 10
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()
    
    def test_negative_discount_raises_error(self):
        """Ensure a ValidationError is raised when the is_discounted_price is negative"""
        
        with self.assertRaises(ValidationError, 
                                msg="Expected a ValidationError because discount price is negative"
                                ):
            # Use Product model directly since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.is_discounted_price = True
            product.discount_price      =  -10
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()

    def test_error_raise_if_discount_price_is_greater_than_price(self):
        """Ensure a ValidationError is raised when the discounted price is greater than the actually price"""

        # This test checks the condition where the discount price is greater than the actual price.
        # If the test passes, it means the logic enforcing this condition is correct.
        #
        # To intentionally create a failure and test whether the validation logic works properly:
        # Comment out the validation lines at 230 and 231 in the product model file, which check if the discount price is less than the actual price.
        # Run the test to confirm if it fails as expected.
        #
        # After the failure is confirmed, uncomment the lines to restore the validation and ensure the logic is working correctly:
        # if self.discount_price >= self.price:
        #     raise ValidationError("Discount price must be less than the actual price.")

        
        with self.assertRaises(ValidationError, 
                                msg="Expected a ValidationError because discount price is greater than the actually price"
                                ):
            # Use Product model directly since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.is_discounted_price = True
            product.price               = 150
            product.discount_price      = 200
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()
    
    def test_negative_weight_error(self):
        """Ensure a ValidationError is raised when the weight is negative"""
        
        with self.assertRaises(ValidationError, 
                                msg="Expected a ValidationError because the weight is negative"
                                ):
            # Use Product model directly since ProductFactory doesn't raise an error
            product = Product(**self.related_fields)
            product.price  = 10
            product.weight = -100
            product.full_clean()  # Validates model constraints, including field-specific validators
            product.save()
            
    def tearDown(self):
        return super().tearDown()