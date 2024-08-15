from django.urls import path

from . import views

urlpatterns = [
   path("account", view=views.account, name="account"),
   path("account/product-management/overview/", view=views.product_management, name="product-management"),
   path("account/product-management/add-new-product/basic-description/", view=views.add_basic_description, name="add_new_product"),
   path("account/product-management/add-new-product/detailed-description/", view=views.add_detailed_description, name="add_detailed_description"),
   path("account/orders/order/", view=views.orders, name="orders"),
   path("account/orders/view-item/<int:id>", views.view_item, name="view-item"),
   path("account/financial-management/overview/", view=views.financial_management, name="financial_management"),
   path("account/orders/order/invoice/<int:item_id>/", view=views.invoice, name="invoice"),
   
]