from django.urls import path

from . import views


urlpatterns = [
   path("", view=views.blog_home_page, name="blog_home"),
 
    
]