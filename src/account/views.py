from django.shortcuts import render, redirect
from django.urls import reverse
from .views_helpers import handle_form
from .forms import BasicFormDescription, DetailedFormDescription, PricingAndInventoryForm

from .utils.converter import convert_decimal_to_float

# Create your views here.


def account(request):
    return render(request, "account/account/account.html")


def product_management(request):
    return render(request, "account/product-management/add-new-product/product-management-overview.html")



def add_basic_description(request):
    return handle_form(
        request=request,
        form_class=BasicFormDescription,
        session_key='basic_form_description',
        next_url_name='detailed_description_form',
        template_name='account/product-management/add-new-product/basic-product-information.html'
    )


def add_detailed_description(request):
    return handle_form(
        request=request,
        form_class=DetailedFormDescription,
        session_key='detailed_form_description',
        next_url_name='pricing_and_inventory_form',
        template_name='account/product-management/add-new-product/detailed-description-specs.html'
    )


def add_pricing_and_inventory(request):
     return handle_form(
        request=request,
        form_class=PricingAndInventoryForm,
        session_key='pricing_and_inventory_form',
        next_url_name='images_and_media_form',
        template_name='account/product-management/add-new-product/pricing-inventory.html'
    )
   
                

def add_images_and_media(request):
    context = {
        "section_id" : "images-and-media",
    }
    return render(request, "account/product-management/add-new-product/images-and-media.html", context=context)


def add_shipping_and_delivery(request):
    context = {
        "section_id" : "shipping-and-delivery",
    }
    return render(request, "account/product-management/add-new-product/shipping-and-delivery.html", context=context)


def add_seo_management(request):
    context = {
        "section_id" : "seo-management",
    }
    return render(request, "account/product-management/add-new-product/SEO-and-meta-information.html", context=context)


def add_additonal_information(request):
    context = {
        "section_id" : "additonal-information",
    }
    return render(request, "account/product-management/add-new-product/additonal-information.html", context=context)


def view_review(request):
    context = {
        "section_id" : "review-section",
        'is_review_section': True
    }
    return render(request, "account/product-management/add-new-product/review-and-submit.html", context=context)
 
 
def view_products(request):
    return render(request, "account/product-management/view-products/view-products.html")
 
 
def orders(request):
    return render(request, "account/orders/orders.html")


def view_item(request, id):
    return render(request, "account/orders/view-item.html")


def financial_management(request):
    return render(request, "account/financial-management/financial-management.html")


def invoice(request, item_id):
    return render(request, "account/orders/invoice.html" )


def refund_overview(request):
    return render(request, "account/refund/refund-management.html")