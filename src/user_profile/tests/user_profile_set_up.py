from django.contrib.auth import get_user_model
from user_profile.models import UserProfile


def set_up_user_profile(username="user", email="egbie@example.com", password="password"):
     User     = get_user_model()
     user     = User.objects.create_user(username=username, 
                                        email=email, 
                                        password=password,
                                        )
     user_profile = UserProfile.objects.get(user=user)
     return user_profile
