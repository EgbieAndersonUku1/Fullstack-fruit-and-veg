from django.test import TestCase
from django.utils import timezone
from time import sleep
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from uuid import uuid4

from product.models import Brand

# Create your tests here.

def get_random_name():
    return f"Test Brand { uuid4() }"

class BrandModelTest(TestCase):
    def setUp(self):
        self.name = "Test Brand"
        self.description = "Test description"
        self.brand = Brand.objects.create(name=self.name, description=self.description)

    def test_single_model_creation_count(self):
        """Test if a single Brand instance is created"""
        EXPECTED_COUNT = 1
        self.assertEqual(Brand.objects.count(), EXPECTED_COUNT)

    def test_brand_name_is_saved_correctly(self):
        """Test if the Brand instance has the correct name and description"""
        brand = Brand.objects.first()

        self.assertIsNotNone(brand, msg="Expected a brand instance but got none")
        self.assertEqual(brand.name, self.name, msg="Brand name does not match expected value")
        self.assertEqual(brand.description, self.description, msg="Brand description does not match expected value")
    
    def test_creation_date_is_automatically_created(self):
        """Test if the brand creation date is automatically set upon creation."""
        
        before_creation_time = timezone.now()
        brand                = Brand.objects.create(name=get_random_name(), description=self.description)
        after_creation_time  = timezone.now()
        
       
        
        self.assertGreaterEqual(brand.created_on, 
                                before_creation_time, 
                                msg="The creation time should not be earlier than the start of the test."
                                )
        
        self.assertLessEqual(self.brand.created_on, 
                             after_creation_time, 
                             msg="The creation time should not be later than the end of the test."
                             )        
        
    
    def test_modified_date_is_only_updated_after_model_change(self):
        """Test if the modified date is updated only when the model is updated."""
       
        brand = Brand.objects.create(name=get_random_name(), description=self.description)
        
        time_before_modification = brand.modified_on
        
        # Ensure the instance and timestamps are valid
        self.assertIsNotNone(brand, msg="The brand instance shouldn't be None")
        self.assertIsNotNone(brand.created_on, msg="Expected 'created_on' to be set, but got None")
        self.assertIsNotNone(time_before_modification, msg="Expected 'modified_on' to be set, but got None")
        
        # Introduce a delay to ensure a measurable time difference
        sleep(0.001)
    
        brand.description = "This is a modified the original description"
        brand.save()
        
        brand.refresh_from_db()
        
        # Assert that modified_on has changed
        self.assertGreater(brand.modified_on, time_before_modification, 
                        msg="Expected 'modified_on' to be updated after saving changes")

    def test_string_method_name(self):
        """Test if the method returns the correct string name"""
        
        EXPECTED_STRING_NAME = self.name
        self.assertEqual(str(self.brand), EXPECTED_STRING_NAME)
    
    def test_string_method_with_special_characters(self):
        """Test if the method returns the correct string for names with special characters."""
        special_name = "Test Brand @2025!"
        self.brand.name = special_name
        self.brand.save()
        
        self.assertEqual(str(self.brand), special_name, msg="The __str__ method did not return the correct value for special characters.")

    
    def test_max_character_name_field(self):
        """Test that the name field does not accept more characters than max_length."""
        
        test_name = "e" * 101  # Create a name longer than 100 characters

        brand = Brand(name=test_name, description=self.description)

        with self.assertRaises(ValidationError):
            brand.full_clean()  # Validates the model's constraints
            brand.save()        # Raise an error if full_clean is skipped
    
    
    def test_blank_description_is_valid(self):
        """Test that blank description is valid"""
        
        brand = Brand.objects.create(name="Test that blank description is valid", description="")
        
        try:
            brand.full_clean()
        except ValidationError:
            self.fail("Blank with blank description should be valid")
            
    def test_null_description_is_valid(self):
        """Test that null desription is valid"""
        
        brand = Brand.objects.create(name="Test that blank description is valid")
        
        try:
            brand.full_clean()
        except ValidationError:
            self.fail("Blank with blank description should be valid")
        
    def test_duplicate_names_is_invalid(self):
        """Test that duplicate names are invalid"""
       
        with self.assertRaises(IntegrityError):
            brand  = Brand.objects.create(name=self.name, description="Duplication description")
            brand.full_clean()
    
    def test_null_name_is_invalid(self):
        """Test that an empty name is invalid."""
        brand = Brand(description=self.description)
        with self.assertRaises(ValidationError):
            brand.full_clean()
    
    def test_null_description_is_valid(self):
        """Test that an empty name is invalid."""
        
        brand = Brand(name=get_random_name(), description=None)
        self.assertIsNotNone(brand)
       
    def test_ordering_is_by_name(self):
        """Test that the default ordering is by name."""
        
        non_alphabetical_product_order = [("Brand Z", "Brand Z description"),
                                          ("Brand A", "Brand A description"), 
                                          ("Brand C", "Brand C description"), 
                                          ("Brand E", "Brand E description")
                                          ]
        
        for (name, description) in non_alphabetical_product_order:
            Brand.objects.create(name=name, description=description)
      

        brand_names = list(Brand.objects.values_list('name', flat=True))
        
        EXPECTED_ALPHABETICALLY_ORDER = ['Brand A', 'Brand C', 'Brand E', 'Brand Z', 'Test Brand']
        self.assertEqual(brand_names, EXPECTED_ALPHABETICALLY_ORDER)
        
        