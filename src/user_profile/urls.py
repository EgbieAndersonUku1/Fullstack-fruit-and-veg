from django.urls import path, include

from . import views



urlpatterns = [

    path('user_profile/', view=views.user_profile, name="user_profile"),
    path("manage_billing_address/", view=views.manage_billing_addresses, name="manage_addresses"),
    path("manage_shipping_address/", view=views.manage_shippng_addresses, name="manage_shippng_addresses"),
    path("mark_as_primary/<id>/", view=views.mark_as_primary_address, name="mark_as_primary"),
    path("delete_address/", view=views.delete_address, name="delete_address"),
]


