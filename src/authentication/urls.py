from django.urls import path

from . import views


urlpatterns = [
     path("validate/password/", view=views.validate_password, name='validate_password'),
     path("register/", view=views.register, name="register"),
    
]