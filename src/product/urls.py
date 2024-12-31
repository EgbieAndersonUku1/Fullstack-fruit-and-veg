from django.urls import path

from . import views


urlpatterns = [
   path("", view=views.product_details, name="product_details"),
  
]