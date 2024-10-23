from django.urls import path

from . import views


urlpatterns = [
     path("subscribe/", view=views.subscribe_user, name='subscribe'),
   
]