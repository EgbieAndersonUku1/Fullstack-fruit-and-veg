from django.urls import path, include

from . import views



urlpatterns = [

    path('user_profile/', view=views.user_profile, name="user_profile"),
    path("manage_address", view=views.manage_address, name="manage_addresses"),
    path("mark_as_primary/<id>/", view=views.mark_as_primary_address, name="mark_as_primary"),
    path("delete_address/<id>/", view=views.delete_address, name="delete_address"),
  
]


