from django.test import TestCase
from django.utils import timezone
from time import sleep
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from uuid import uuid4

from product.models import Category

# Create your tests here.

def get_category_name():
    return f"Test Category { uuid4() }"


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category_name = "Test Category"
        self.description   = "Test description"
        self.category      = Category.objects.create(category=self.category_name, description=self.description)

    def test_single_model_creation_count(self):
        """Test if a single Category instance is created"""
        EXPECTED_COUNT = 1
        self.assertEqual(Category.objects.count(), EXPECTED_COUNT)

    def test_category_name_is_saved_correctly(self):
        """Test if the Category instance has the correct name and description"""
        category = Category.objects.first()

        self.assertIsNotNone(category, msg="Expected a category instance but got none")
        self.assertEqual(category.category, self.category_name, msg="Category name does not match expected value")
        self.assertEqual(category.description, self.description, msg="Category description does not match expected value")
    
    def test_creation_date_is_automatically_created(self):
        """Test if the category creation date is automatically set upon creation."""
        
        before_creation_time = timezone.now()
        category             = Category.objects.create(category=get_category_name(), description=self.description)
        after_creation_time  = timezone.now()
        
       
        
        self.assertGreaterEqual(category.created_on, 
                                before_creation_time, 
                                msg="The creation time should not be earlier than the start of the test."
                                )
        
        self.assertLessEqual(self.category.created_on, 
                             after_creation_time, 
                             msg="The creation time should not be later than the end of the test."
                             )        
        
    
    def test_modified_date_is_only_updated_after_model_change(self):
        """Test if the modified date is updated only when the model is updated."""
       
        category = Category.objects.create(category=get_category_name(), description=self.description)
        
        time_before_modification = category.modified_on
        
        # Ensure the instance and timestamps are valid
        self.assertIsNotNone(category, msg="The category instance shouldn't be None")
        self.assertIsNotNone(category.created_on, msg="Expected 'created_on' to be set, but got None")
        self.assertIsNotNone(time_before_modification, msg="Expected 'modified_on' to be set, but got None")
        
        # Introduce a delay to ensure a measurable time difference
        sleep(0.001)
    
        category.description = "This is a modified the original description"
        category.save()
        
        category.refresh_from_db()
        
        # Assert that modified_on has changed
        self.assertGreater(category.modified_on, time_before_modification, 
                        msg="Expected 'modified_on' to be updated after saving changes")

    def test_string_method_name(self):
        """Test if the method returns the correct string name"""
        
        EXPECTED_STRING_NAME = self.category_name
        self.assertEqual(str(self.category), EXPECTED_STRING_NAME)
    
    def test_string_method_with_special_characters(self):
        """Test if the method returns the correct string for names with special characters."""
        special_name           = "Test Category @2025!"
        self.category.category = special_name
        self.category.save()
        self.category.refresh_from_db()
        
        self.assertEqual(str(self.category), special_name, msg="The __str__ method did not return the correct value for special characters.")

    def test_max_character_name_field(self):
        """Test that the name field does not accept more characters than max_length."""
        
        test_name = "e" * 101  # Create a name longer than 100 characters

        category = Category(category=test_name, description=self.description)

        with self.assertRaises(ValidationError):
            category.full_clean()  # Validates the model's constraints
            category.save()        # Raise an error if full_clean is skipped
    
    
    def test_blank_description_is_valid(self):
        """Test that blank description is valid"""
        
        category = Category.objects.create(category="Test that blank description is valid", description="")
        
        try:
            category.full_clean()
        except ValidationError:
            self.fail("Blank with blank description should be valid")
            
    def test_null_description_is_valid(self):
        """Test that null desription is valid"""
        
        category = Category.objects.create(category="Test that blank description is valid")
        
        try:
            category.full_clean()
        except ValidationError:
            self.fail("Blank with blank description should be valid")
        
    def test_duplicate_names_is_invalid(self):
        """Test that duplicate names are invalid"""
       
        with self.assertRaises(IntegrityError):
            Category.objects.create(category=self.category, description="Duplication description")
           
    def test_null_name_is_invalid(self):
        """Test that an empty name is invalid."""
        
        category = Category(description=self.description)
        with self.assertRaises(ValidationError):
            category.full_clean()
    
    def test_null_description_is_valid(self):
        """Test that an empty name is invalid."""
        
        category = Category(category=get_category_name(), description=None)
        self.assertIsNotNone(category)
   
    def test_ordering_is_by_name(self):
        """Test that the default ordering is by category."""
        
        non_alphabetical_product_order = [("Category Z", "Category Z description"),
                                          ("Category A", "Category A description"), 
                                          ("Category C", "Category C description"), 
                                          ("Category E", "Category E description")
                                          ]
        
        for (name, description) in non_alphabetical_product_order:
            Category.objects.create(category=name, description=description)
      

        category_names= list(Category.objects.values_list('category', flat=True))
        
        EXPECTED_ALPHABETICALLY_ORDER = ['Category A', 'Category C', 'Category E', 'Category Z', 'Test Category']
        self.assertEqual(category_names, EXPECTED_ALPHABETICALLY_ORDER)