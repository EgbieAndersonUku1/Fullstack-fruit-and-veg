from django.test import TestCase
from django.urls import reverse


from django.contrib.auth import get_user_model
from user_profile.models import UserProfile

User = get_user_model()


    
class UserProfileViewsTest(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.profile_url = reverse('user_profile')  
        login_success = self.client.login(email='testuser@example.com', password='password123')
      
        self.assertTrue(login_success, "User login failed")

    def test_user_profile_view_get(self):
       
        response = self.client.get(self.profile_url)

        # Check response status and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/user_profile.html')  
    
  
        
        