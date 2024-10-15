from django.urls import path

from . import views


urlpatterns = [
   
   path("reviews/", views.reviews_section, name="reviews"),
   path("add/", view=views.add_testimonial, name="add-testimonial"),
   path("all/", view=views.all_reviews, name="all-reviews"),
   path("display/", view=views.display_testimonial, name="display-testimonial"),
    
]