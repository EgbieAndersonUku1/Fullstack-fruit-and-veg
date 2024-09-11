from django.test import TestCase
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile


class UserProfileCreationTests(TestCase):
    
    def setUp(self):
        self.User     = get_user_model()
        self.username = "user"
        self.email    = "egbie@example.com"
        self.password = "password"
    
    def test_is_user_profile_created_when_a_new_user_is_created(self):
        """Test if a user profile is automatically created when a new user is created."""
        
        # Verify that no user profile exists initially
        user_profile_count = UserProfile.objects.count()
        self.assertEqual(user_profile_count, 0)
        
        # Create a new user
        self.User.objects.create_user(username=self.username, email=self.email, password=self.password)
        
        # Check if a user profile was created
        new_user_profile = UserProfile.objects.first()
        self.assertIsNotNone(new_user_profile)
        
        # Verify that the user profile is linked to the right user
        user = self.User.objects.get(email=self.email)
        self.assertEqual(new_user_profile.user, user)
        
        # Verify that there is exactly one user profile now
        user_profile_count = UserProfile.objects.count()
        self.assertEqual(user_profile_count, 1)
        
    def test_profile_creation_for_different_user_types(self):
        """Test user profile creation for different user types (regular vs. superuser)."""
        
        email = "super_user@example.com"
        
        # Verify that no superuser profile exists initially
        user_profile_count = UserProfile.objects.count()
        self.assertEqual(user_profile_count, 0)
        
        # Create a superuser
        self.User.objects.create_superuser(username="super_user", email=email, password="password")
       
        # Verify that a superuser profile was created
        user_profile_count = UserProfile.objects.count()
        self.assertEqual(user_profile_count, 1)
        
        # Verify that the profile is linked to the right user
        super_user_profile = UserProfile.objects.first()
        user               = self.User.objects.get(email=email)
        self.assertEqual(super_user_profile.user, user)
    
    def tearDown(self):
        # Clean up any data created after every test
        UserProfile.objects.all().delete()
        self.User.objects.all().delete()


class UserProfileMethodTests(TestCase):
    
    def setUp(self):
        self.User         = get_user_model()
        self.username     = "user"
        self.email        = "egbie@example.com"
        self.password     = "password"
        self.user         = self.User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.user_profile = UserProfile.objects.get(user=self.user)

    def test_if_user_profile_can_be_retrieved_from_user(self):
        """Test if the UserProfile can be retrieved from the User."""
        
        # Retrieve the associated UserProfile
        user_profile = UserProfile.objects.filter(user=self.user).first()
        
        # Ensure the UserProfile is not None
        self.assertIsNotNone(user_profile)
        
        # Verify that the UserProfile is associated with the correct user
        self.assertEqual(user_profile.user, self.user)
    
    def test_full_name_method(self):
        """Test if the full name is returned correctly by the method."""
        
        # Define expected full name
        EXPECTED_VALUE = "Super User"
        
        # Update user profile details
        self.user_profile.first_name = "super"
        self.user_profile.last_name  = "user"
        self.user_profile.save()
        
        # Test that the full_name method returns the expected value
        self.assertEqual(self.user_profile.full_name, EXPECTED_VALUE)
        
    def test_full_name_method_with_empty_names(self):
        """Test if the full name is handled correctly when first or last name is empty."""
        
        # Test different empty name scenarios
        self.user_profile.first_name = ""
        self.user_profile.last_name  = "user"
        self.user_profile.save()
        self.assertEqual(self.user_profile.full_name, "")
        
        self.user_profile.first_name = "super"
        self.user_profile.last_name  = ""
        self.user_profile.save()
        self.assertEqual(self.user_profile.full_name, "")
        
        self.user_profile.first_name = "super"
        self.user_profile.last_name  = ""
        self.user_profile.save()
        self.assertEqual(self.user_profile.full_name, "")
    
    def test_username_property(self):
        """Test if the username property returns the correct username."""
        
        self.assertEqual(self.user_profile.username, self.username.title())

    def test__str__method(self):
        """Test the string representation of the user profile."""
        
        # Check that the string representation matches the expected format
        self.assertEqual(str(self.user_profile), f"Profile for {self.user.username}")

    def tearDown(self):
        # Clean up any data created after every test
        UserProfile.objects.all().delete()
        self.User.objects.all().delete()