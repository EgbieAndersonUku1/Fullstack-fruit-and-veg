from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.utils import timezone

from testimonal.models import Testimonial
from django.contrib.auth import get_user_model
from testimonal.signals import pre_save_testimonial

User = get_user_model()


TESTIMONIAL_ATTRIBRUTES = {
     "user_image"       : "https://some/url/image/link/here/",
     "testimonial_text" : "This is a testimonial text",
     "ratings"          :  5,
     "company_name"     : "test company name",
     "Country"          : "Test country",
     "location"         : "Test location",
}


def create_new_user(username:str="testimonial_user", email:str="testimonial@example.com", password:str="pa$$word1"):
    """
    Creates a new user and returns the instance.
    
    Parameters:
        - username (str, optional): The username for the new user. Defaults to 'testimonial_user'.
        - email (str, optional): The email for the new user. Defaults to 'testimonial@example.com'.
        - password (str, optional): The password for the new user. Defaults to 'pa$$word1'.
    
    Returns:
        User: The created user instance.
    """
    user = User.objects.create_user(username=username,
                        email=email,
                        password=password
                        )
    return user
 
 
def create_new_testimonial(author, title:str="Testimonial test",  **kwargs:any) -> Testimonial:
     """
     Creates a new testimonial model for a given user. The function takes an author,
     a title, testimonial_text and dictionary containing arguments that will be used
     to create the Testimonial model
     
     :Parameters:
        - author (user object): The object containing the user object
        - title(str, optional): The title for the testimonial text.
        - **kwargs: Containing a dictionary of keyword arguments that will be used for the Testimonial   
     """
     
     user_image        = kwargs.get("user_image", "https://some/url/image/link/here/")
     testimonial_text  = kwargs.get("testimonial_text", "This is a testimonial text")
     ratings           = kwargs.get("ratings", 5)
     company_name      = kwargs.get("company_name", "test company name")
     country           = kwargs.get("Country", "Test country")
     location          = kwargs.get("location", "Test location")
     
     if not isinstance(author, User):
         raise ValueError("The author is not an instance of the User model")
     
     testimonial = Testimonial.objects.create(
         author=author,
         title=title,
         user_image=user_image,
         testimonial_text=testimonial_text,
         ratings=ratings,
         company_name=company_name,
         country=country,
         location=location
     )
     return testimonial
         
    

def create_multiple_testimonials(num_of_testimonials_to_create:int=5)-> None:
    """
    A function that when called creates multiple testimonials with the database.
    
    Returnns:
        - The function does not return anything but instead creates multiple testimonials with
          the database
    
    """
    if not isinstance(num_of_testimonials_to_create, (int, float)):
        raise TypeError("The parameter for the number of testimonials to create must be an integer ")
        
    for i in range(num_of_testimonials_to_create):
         number = i + 1
         user_attributes = [{"username": f"username{number}", "email": f"user{number}@example.com", "password": f"password{number}"}]

         for user_attr in user_attributes:
            user = create_new_user(username=user_attr["username"],
                            email=user_attr["email"],
                            password=user_attr["password"],
                            )
            title = f"Testimonal test {number + 1}"
            create_new_testimonial(user, title, **TESTIMONIAL_ATTRIBRUTES)
    
        
# Create your tests here.
class TestimonialTests(TestCase):
    def setUp(self):
        self.testimonial_user = create_new_user()
        self.testimonial      = create_new_testimonial(author=self.testimonial_user, **TESTIMONIAL_ATTRIBRUTES)
           
    def test_object_creation(self):
        """Test if the user and testimonial models have been created"""
        testimonial_count = Testimonial.objects.count()
        user_count        = User.objects.count()
        
        self.assertIsNotNone(self.testimonial_user)
        self.assertIsNotNone(self.testimonial)
        self.assertEqual(testimonial_count, 1)
        self.assertEqual(user_count, 1)

    def test_testimonial_field_attributes(self):
        """Test if the attributes for the testimonial is correctly created"""
        
        self.testimonial.refresh_from_db()
        USER_IMAGE_LINK  = "https://some/url/image/link/here/"
        TESTIMONIAL_TEXT = "This is a testimonial text"
        RATINGS          = 5
        COMPANY_NAME     = "test company name"
        COUNTRY          = "Test country"
        LOCATION         = "Test location"
        
        self.assertIsNotNone(self.testimonial)
        self.assertEqual(self.testimonial.author, self.testimonial_user)
        self.assertEqual(self.testimonial.user_image, USER_IMAGE_LINK)
        self.assertEqual(self.testimonial.testimonial_text, TESTIMONIAL_TEXT)
        self.assertEqual(self.testimonial.ratings, RATINGS)
        self.assertEqual(self.testimonial.company_name, COMPANY_NAME)
        self.assertEqual(self.testimonial.country, COUNTRY)
        self.assertEqual(self.testimonial.location, LOCATION)
        
    def test__str__representation(self):
        """Test if it returns the correct representation of the testimonial string"""
        EXPECTED_STR = f"{self.testimonial.author} - {self.testimonial.title[:50]}"
        self.assertEqual(str(self.testimonial), EXPECTED_STR)
    
    def test_date_created(self):
        """Test if the date is automatically created when a testimonial object is created"""
        self.testimonial.refresh_from_db()
        current_time_now = timezone.now()
        self.assertLessEqual(self.testimonial.date_created, current_time_now)
    
    def test_date_sent(self):
        """Test if the date is automatically created when a testimonial object is created"""
        self.testimonial.refresh_from_db()
        current_time_now = timezone.now()
        self.assertLessEqual(self.testimonial.date_sent, current_time_now)
    
    def test_missing_title_field(self):
        """Test that missing the title field in Testimonial raises ValidationError."""
        new_user = create_new_user(username="test_user20", email="test_user20@example.com")
        
        testimonial = Testimonial(
            author=new_user,
            title="",  # Title is empty
            user_image="valid_image.jpg",
            testimonial_text="Valid testimonial text",
            ratings="5",
            country="Valid country",
            location="Valid location"
        )
        
        with self.assertRaises(ValidationError):
            testimonial.full_clean()
        
    def test_missing_testimonial_text_field(self):
        """Test that missing the testimonial_text field in Testimonial raises ValidationError."""
        new_user = create_new_user(username="test_user20", email="test_user20@example.com")
        
        testimonial = Testimonial(
            author=new_user,
            title="Valid title",
            user_image="valid_image.jpg",
            testimonial_text="",  # Testimonial text is empty
            ratings="5",
            country="Valid country",
            location="Valid location"
        )
        
        with self.assertRaises(ValidationError):
            testimonial.full_clean()

    def test_missing_ratings_field(self):
        """Test missing rating in Testimonial raises ValidationError."""
        new_user = create_new_user(username="test_user20", email="test_user20@example.com")
        
        testimonial = Testimonial(
            author=new_user,
            title="Valid title",
            user_image="valid_image.jpg",
            testimonial_text="some random text to test",  
            ratings="", # rating is missing
            country="Valid country",
            location="Valid location"
        )
        
        with self.assertRaises(ValidationError):
            testimonial.full_clean()
    
    def test_missing_country_field(self):
        """Test missing country in Testimonial raises ValidationError."""
        new_user = create_new_user(username="test_user20", email="test_user20@example.com")
        
        testimonial = Testimonial(
            author=new_user,
            title="Valid title",
            user_image="valid_image.jpg",
            testimonial_text="some random text to test",  
            ratings="5", 
            country="", # country is missing
            location="Valid location"
        )
        
        with self.assertRaises(ValidationError):
            testimonial.full_clean()
    
    def test_missing_location_field(self):
        """Test missing location in Testimonial raises ValidationError."""
        new_user = create_new_user(username="test_user20", email="test_user20@example.com")
        
        testimonial = Testimonial(
            author=new_user,
            title="Valid title",
            user_image="valid_image.jpg",
            testimonial_text="some random text to test",  
            ratings="5", 
            country="UK",
            location="" # location is missing
        )
        with self.assertRaises(ValidationError):
            testimonial.full_clean()
            
    def test_if_featured_checkmark_creation_is_false(self):
        """Test that when the testimonial oject is created that it is not created as featured"""
        self.testimonial.refresh_from_db()
        self.assertFalse(self.testimonial.featured)
    
    def test_get_by_user_model(self):
        """Test if the 'get_by_user' method correctly retrieves the testimonial object via the method"""
        
        # create a user that hasn't written a testimonial
        user = create_new_user(username="non-existance-user",
                               email="non-existance-user@example.com",
                               password="password1"
                               )
        self.assertIsNotNone(user)
        
        # now attempt to get the testimonial for non-existent user that has created a testimonial
        testimonial = Testimonial.get_by_user(user)
        self.assertIsNone(testimonial)
        
        # now attempt to get the testimonial for a user that has created a testimonial
        existing_testimonial = Testimonial.get_by_user(self.testimonial_user)
        self.assertIsNotNone(existing_testimonial)
        
        # check if the testimonial belongs to the attended user
        self.assertEqual(existing_testimonial.author, self.testimonial_user)
        
    def test_if_multiple_testimonials_can_be_created(self):
        """Test if the Testimonial is able to create multiple testimonials in the database"""
        
        create_multiple_testimonials()
        
        testimonial_count    = Testimonial.objects.count()
        user_creation_count  = User.objects.count()
        
        # one creation in the setup and six new created testimonials when the model is created
        EXPECTED_CREATION_COUNT = 6
        
        self.assertEqual(testimonial_count, EXPECTED_CREATION_COUNT, f"The count should be 6 not {testimonial_count}")
        self.assertEqual(user_creation_count, EXPECTED_CREATION_COUNT, f"The count should be 6 not {user_creation_count}")
    
    def test_if_admin_can_response(self):
        """Test if the admin can post a response in response to a given Testimonial."""
        
        # Disconnect the pre_save signal to prevent it from sending the email
        pre_save.disconnect(pre_save_testimonial, sender=Testimonial)
        
        try:
            EXPECTED_ADMIN_RESPONSE = "Thank you"
            self.testimonial.admin_response = EXPECTED_ADMIN_RESPONSE
            self.testimonial.save()

            self.testimonial.refresh_from_db()

            # Check if the response was saved correctly without triggering the pre_save signal
            self.assertEqual(self.testimonial.admin_response, EXPECTED_ADMIN_RESPONSE)
        
        finally:
            # Reconnect the signal after the test
            pre_save.connect(pre_save_testimonial, sender=Testimonial)       
    
    def test_if_admin_can_approve_testimonial(self):
        """Test if the admin can approval a testimonial"""
        
        # Disconnect the pre_save signal to prevent it from sending the email
        pre_save.disconnect(pre_save_testimonial, sender=Testimonial)
        
        try:
            
            # first check if is_approved hasn't be approved yet
            self.assertFalse(self.testimonial.is_approved)
            
            self.testimonial.is_approved = True
            self.testimonial.save()

            self.testimonial.refresh_from_db()

            # Check if the is_approved was checked
            self.assertTrue(self.testimonial.is_approved)
        
        finally:
            # Reconnect the signal after the test
            pre_save.connect(pre_save_testimonial, sender=Testimonial)       
            
    def tearDown(self) -> None:
        Testimonial.objects.all().delete()
        User = get_user_model()
        User.objects.all().delete()
        
        

