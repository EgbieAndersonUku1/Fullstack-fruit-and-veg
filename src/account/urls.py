from django.urls import path

from . import views

urlpatterns = [
   path("account", view=views.account, name="account"),
   path("account/product-management/", view=views.product_management, name="product-management"),
   path("account/product-management/add-new-product/basic-description/", view=views.add_basic_description, name="add_new_product"),
   path("account/product-management/add-new-product/detailed-description/", view=views.add_detailed_description, name="add_detailed_description")
   
]