from django.urls import path

from . import views


urlpatterns = [
   path("", view=views.blog_home_page, name="blog_home"),
   path("/<int:blog_id>/", view=views.blog_details, name="blog_details"),
 
    
]