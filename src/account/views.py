from django.shortcuts import render, redirect
from django.urls      import reverse

from .views_helpers   import handle_form
from .forms.forms     import (BasicFormDescription, 
                              DetailedFormDescription,
                              PricingAndInventoryForm, 
                              ImageAndMediaForm, 
                              ShippingAndDeliveryForm,
                              SeoAndMetaForm,
                              AdditionalInformationForm,
                              )
from .utils.utils     import create_unique_file_name, save_file_temporarily


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
        template_name='account/product-management/add-new-product/basic-product-information.html',
      
    )


def add_detailed_description(request):
    return handle_form(
        request=request,
        form_class=DetailedFormDescription,
        session_key='detailed_form_description',
        next_url_name='pricing_and_inventory_form',
        template_name='account/product-management/add-new-product/detailed-description-specs.html',
        checkbox_fields_to_store=("size", "color")
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
    
    context      = {"section_id" : "images-and-media"}
    initial_data = request.session.get("temp_file_paths", {})
    form         = ImageAndMediaForm(initial=initial_data)
    
    if request.method == "POST":
        
        form = ImageAndMediaForm(request.POST, request.FILES)
        if form.is_valid():
    
            if form.has_changed():
                
                file_fields     = ['primary_image', 'side_image1', 'side_image2', 'primary_video']
                temp_file_paths = {}
                
                for field in file_fields:
                    if field in request.FILES:
                        temp_file_paths[field] = save_file_temporarily(request.FILES[field])
                request.session["temp_file_paths"] = temp_file_paths
                
            return redirect(reverse("shipping_and_delivery_form"))
    
    context["form"] = form
    return render(request, "account/product-management/add-new-product/images-and-media.html", context=context)


def add_shipping_and_delivery(request):
    return handle_form(request=request,
                       form_class=ShippingAndDeliveryForm,
                       session_key="shipping_and_delivery",
                       next_url_name="seo_and_meta_form",
                       template_name="account/product-management/add-new-product/shipping-and-delivery.html",
                       checkbox_fields_to_store=("shipping")
                       )



def add_seo_management(request):
    return handle_form(request=request,
                       form_class=SeoAndMetaForm,
                       session_key="seo_management",
                       next_url_name="add_information_form",
                       template_name="account/product-management/add-new-product/SEO-and-meta-information.html",
                       )


def add_additonal_information(request):
    return handle_form(request=request,
                       form_class=AdditionalInformationForm,
                       session_key="additional_information",
                       next_url_name="view_review",
                       template_name="account/product-management/add-new-product/additonal-information.html",
                       )


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