from django.urls import path

from . import views


urlpatterns = [
     path("validate/password/", view=views.validate_password, name='validate_password'),
     path("validate/username/", view=views.validate_username, name='validate_username'),
     path("validate/email/", view=views.validate_email, name='validate_email'),
     path("verify/<username>/<token>/", view=views.verify_email_token, name="verify_email"),
     path("register/", view=views.register, name="register"),
     path("login/", view=views.user_login, name="login"),
     path("logout", views.user_logout, name="logout"),
    
]