from django.urls import path, include

from . import views



urlpatterns = [

    path('user_profile/', view=views.user_profile, name="user_profile"),
  
]


