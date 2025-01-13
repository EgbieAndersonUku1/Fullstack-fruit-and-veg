from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from uuid import uuid4

from product.models import ProductVariation, Product, Category, Manufacturer
from product.tests.factory import CategoryFactory, ProductFactory


# Create your tests here.
class ProductModelTest(TestCase):
  
    def test_single_product_creation(self):
        """Test if a single product has been created and saved in the database"""
        
        EXPECTED_NAME = "Test Product"
        product       = ProductFactory(name="Test Product")
        self.assertEqual(product.name, EXPECTED_NAME)
        
        # Test if it was saved to the database
        product_in_db = Product.objects.filter(name=product.name).exists()
        self.assertTrue(product_in_db)

    def test_if_product_with_custom_name_is_created(self):
        """Test if a product with a custom name is created and saved in the database"""
        
        EXPECTED_NAME = "Unique Product"
        product       = ProductFactory(name=EXPECTED_NAME)
        
        self.assertEqual(product.name, EXPECTED_NAME)
        
        # Test if it was saved to the database
        product_in_db = Product.objects.filter(name=product.name).exists()
        self.assertTrue(product_in_db)

    def test_if_product_with_custom_description_is_created(self):
        """Test if a product with a custom name is created and saved in the database"""
        
        EXPECTED_DESC = "Unique Product description"
        product       = ProductFactory(long_description=EXPECTED_DESC)
        
        self.assertEqual(product.long_description, EXPECTED_DESC)
        
        # Test if it was saved to the database
        product_in_db = Product.objects.get(name=product.name)
        self.assertEqual(product.long_description, product_in_db.long_description)
