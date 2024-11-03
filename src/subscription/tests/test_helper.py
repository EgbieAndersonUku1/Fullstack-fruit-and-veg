from django.contrib.auth import get_user_model

User = get_user_model()


def create_test_user(username="test_username", email="test_subscription@example.com", password="password!") -> "User":
    """
    Creates a test user that will be used for testing.
    
    :Params:
        username (str): The username that will be created for the user
        email    (str): The email address that will be created  for the suer
        password (str): The password that will be created for the suer
    
    :Returns
        - Returns an instance of the User model
    """
    user = User.objects.create(username=username, 
                               email=email,
                               )
    user.set_password(password)
    return user

