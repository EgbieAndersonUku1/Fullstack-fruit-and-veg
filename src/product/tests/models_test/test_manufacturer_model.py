from django.test import TestCase
from django.utils import timezone
from time import sleep
from django.db.utils import IntegrityError
from django.db.utils import DataError

from uuid import uuid4

from product.models import Manufacturer

# Create your tests here.

def get_random_name():
    return f"Test Brand { uuid4() }"


def create_test_manufacturer(
    name: str, 
    description: str = "Test manufacturer description", 
    address: str = "Test manufacturer address", 
    is_certified: bool = True, 
    contact_num: str = "020-7147-999"
):
    """
    Creates and returns a new instance of the Manufacturer model.

    Args:
        name (str): The name of the manufacturer. This is a required field.
        description (str, optional): A description of the manufacturer. Defaults to None.
        address (str, optional): The address of the manufacturer. Defaults to None.
        is_certified (bool, optional): Whether the manufacturer is certified. Defaults to True.
        contact_num (str, optional): The contact number of the manufacturer. Defaults to None.

    Returns:
        Manufacturer: A new instance of the Manufacturer model.

    Example usage:
        >>> manufacturer = create_test_manufacturer(
        ...     name="Test Manufacturer", 
        ...     description="A test manufacturer", 
        ...     address="123 Test St", 
        ...     is_certified=False, 
        ...     contact_num="123-456-7890"
        ... )
    """
    return Manufacturer.objects.create(
        name=name,
        description=description,
        address=address,
        is_certified=is_certified,
        contact_num=contact_num,
    )


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.name        = "Test manufacturer"
        self.description = "Test manufacturer description"
        self.address     = "Test manufacturer address"
        self.contact_num = "020-7147-999"
        
        self.manufactuer = create_test_manufacturer(self.name)
    
    def test_single_creation(self):
        """Test if a single model object has been created in the database"""
        
        EXPECTED_COUNT = 1
        self.assertEqual(Manufacturer.objects.count(), EXPECTED_COUNT, msg="Expected a single creation count")
    
    def test_name_field_is_created(self):
        """Test if the name field was successfully created"""
        
        self.manufactuer.refresh_from_db()
        self.assertEqual(self.manufactuer.name, 
                         self.name, 
                         msg="Expected the name to match but the names does not match with the test name")
    
    
    def test_description_field_is_created(self):
        """Test if the name field was successfully created"""
        
        self.manufactuer.refresh_from_db()
        self.assertEqual(self.manufactuer.description, 
                         self.description, 
                         msg="Expected the description field to match but the description does not match with the test description")
    
    def test_address_field_is_created(self):
        """Test if the name field was successfully created"""
        
        self.manufactuer.refresh_from_db()
        self.assertEqual(self.manufactuer.address, 
                         self.address, 
                         msg="Expected the address to match but the address does not match with the test address")
    
    def test_that_is_certified_is_created_and_set_to_true(self):
        """Test that the certified field is created and the default is set to True"""
        self.assertTrue(self.manufactuer.is_certified)
    
    def test_creation_date_is_automatically_created(self):
        """Test if the Maufacuter creation date is automatically set upon creation."""
        
        before_creation_time = timezone.now()
        manufacturer         = create_test_manufacturer(name=get_random_name())
        after_creation_time  = timezone.now()
        
        self.assertGreaterEqual(manufacturer.created_on, 
                                before_creation_time, 
                                msg="The creation time should not be earlier than the start of the test."
                                )
        
        self.assertLessEqual(self.manufactuer.created_on, 
                             after_creation_time, 
                             msg="The creation time should not be later than the end of the test."
                             )        
        
    
    def test_modified_date_is_only_updated_after_model_change(self):
        """Test if the modified date is updated only when the model is updated."""
       
        manufacturer= create_test_manufacturer(name=get_random_name())
        
        time_before_modification = manufacturer.modified_on
        
        # Ensure the instance and timestamps are valid
        self.assertIsNotNone(manufacturer, msg="The manufacturer instance shouldn't be None")
        self.assertIsNotNone(manufacturer.created_on, msg="Expected 'created_on' to be set, but got None")
        self.assertIsNotNone(time_before_modification, msg="Expected 'modified_on' to be set, but got None")
        
        # Introduce a delay to ensure a measurable time difference
        sleep(0.001)
    
        manufacturer.description = "This is a modified the original description"
        manufacturer.save()
        
        manufacturer.refresh_from_db()
        
        # Assert that modified_on has changed
        self.assertGreater(manufacturer.modified_on, time_before_modification, 
                        msg="Expected 'modified_on' to be updated after saving changes")

    def test_string_method_name(self):
        """Test if the method returns the correct string name"""
        
        EXPECTED_STRING_NAME = self.manufactuer.name
        self.assertEqual(str(self.manufactuer), EXPECTED_STRING_NAME)
    
    def test_string_method_with_special_characters(self):
        """Test if the method returns the correct string for names with special characters."""
        
        special_name           = "Test Manufacturer @2025!"
        self.manufactuer.name  = special_name
        self.manufactuer.save()
        self.manufactuer.refresh_from_db()
        
        self.assertEqual(str(self.manufactuer), special_name, msg="The __str__ method did not return the correct value for special characters.")

    def test_max_character_name_field(self):
        """Test that the name field does not accept more characters than max_length."""
        
        test_name = "e" * 256  # Create a name longer than 255 characters
        
        # Assert that creating a manufacturer with a name longer than 255 characters raises a DataError
        with self.assertRaises(DataError):
            create_test_manufacturer(name=test_name)
         
    def test_blank_description_is_valid(self):
        """Test that blank description is valid"""
        
        create_test_manufacturer(name=get_random_name(), description="")
       
    def test_null_description_is_valid(self):
        """Test that null desription is valid"""
                
        create_test_manufacturer(name=get_random_name(), description=None)
       
    def test_duplicate_names_is_invalid(self):
        """Test that duplicate names are invalid"""
       
        with self.assertRaises(IntegrityError):
            duplicate_name = self.name
            create_test_manufacturer(name=duplicate_name)
           
    def test_null_name_is_invalid(self):
        """Test that an empty name is invalid."""
    
        with self.assertRaises(IntegrityError):
            create_test_manufacturer(name=None) 
   
    