from django.test import TestCase
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile
from .user_profile_set_up import set_up_user_profile

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
    
    def test_user_delete_cascades_to_user_profile(self):
        """Test that when a user is deleted, the user profile is automatically deleted as well"""
        
        # Create a new user
        new_user = self.User.objects.create_user(username="new user", email="new_user@example.com", password="password")
        self.assertIsNotNone(new_user)
        
        new_user_profile    = UserProfile.objects.filter(user=new_user).first()
        new_user_profile_id = new_user_profile.id
        self.assertIsNotNone(new_user_profile)
        
        new_user.delete()
        
        # Verify that the UserProfile was also deleted
        new_user_profile = UserProfile.objects.filter(id=new_user_profile_id).first()
        self.assertIsNone(new_user_profile)

    def test_superuser_delete_cascades_to_user_profile(self):
        """Test that when a superuser is deleted, the associated user profile is automatically deleted as well."""
        
        # Create a new superuser
        new_super_user = self.User.objects.create_superuser(username="super new user", email="super_user@example.com", password="password")
        self.assertIsNotNone(new_super_user)
        
        # Check that the UserProfile was created
        new_user_profile = UserProfile.objects.filter(user=new_super_user).first()
        profile_id       = new_user_profile.id
        self.assertIsNotNone(new_user_profile)
        
        new_super_user.delete()
        
        # Verify that the UserProfile was also deleted
        new_user_profile = UserProfile.objects.filter(id=profile_id)
        self.assertFalse(new_user_profile.exists())
       
    
    def test_deleting_user_profile_does_not_delete_user(self):
        """Ensure that deleting a UserProfile does not delete the associated User."""
        
        USERNAME = "test profile"
        
        # create a user profile
        new_profile = set_up_user_profile(username=USERNAME, email="test_profile@example.com", password="password")
        
        newly_created_user    = self.User.objects.filter(username=USERNAME).first()
        newly_created_user_id = newly_created_user.id
        self.assertIsNotNone(newly_created_user)

        new_profile.delete()
        
        # verify that the user profile is deleted
        user_profile = UserProfile.objects.filter(id=newly_created_user_id)
        self.assertFalse(user_profile.exists())
        
        # check if the user model still exists after deleting new_profile
        newly_created_user = self.User.objects.filter(username=USERNAME)
        self.assertTrue(newly_created_user.exists(), "The user model should not be deleted")

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