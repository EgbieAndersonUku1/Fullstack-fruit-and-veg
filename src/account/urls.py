from django.urls import path

from . import views

urlpatterns = [
   path("", view=views.account, name="account"),
   path("landing-page/", view=views.landing_page, name="landing-page"),
   path("product-management/overview/", view=views.product_management, name="product-management"),
   path("product-management/add-new-product/basic-description/", view=views.add_basic_description, name="basic_description_form"),
   path("product-management/add-new-product/detailed-description/", view=views.add_detailed_description, name="detailed_description_form"),
   path("product-management/add-new-product/pricing-and-inventory/", view=views.add_pricing_and_inventory, name="pricing_and_inventory_form"),
   path("product-management/add-new-product/images-and-media/", view=views.add_images_and_media, name="images_and_media_form"),
   path("product-management/add-new-product/shipping-and-delivery/", view=views.add_shipping_and_delivery, name="shipping_and_delivery_form"),
   path("product-management/add-new-product/seo/", view=views.add_seo_management, name="seo_and_meta_form"),
   path("product-management/add-new-product/nutrition/", view=views.add_nutrition, name="nutrition_form"),
   path("product-management/add-new-product/additional-information/", view=views.add_additonal_information, name="add_information_form"),
   path("product-management/add-new-product/review-and-submit/", view=views.view_review, name="view_review"),
   path("product-management/add-new-product/save-product-form/", view=views.process_and_save_product_form, name="process_form"),
   path("product-management/add-new-product/view-products/", view=views.view_products, name="view_products"),
   path("orders/order/", view=views.orders, name="orders"),
   path("orders/view-item/<int:id>", views.view_item, name="view-item"),
   path("financial-management/overview/", view=views.financial_management, name="financial_management"),
   path("orders/order/invoice/<int:item_id>/", view=views.invoice, name="invoice"),
   path("refund-management/overview", view=views.refund_overview, name="refund-overview"),
 
   
]