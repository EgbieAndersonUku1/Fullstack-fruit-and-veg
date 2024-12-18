from django.shortcuts import render, redirect
from django.urls      import reverse
from django.conf      import settings
from django.contrib.auth.decorators import login_required

from account.utils.utils import save_file_temporarily
from authentication.forms.login_form import LoginForm

from .views_helpers   import handle_form
from .forms.forms     import (BasicFormDescription, 
                              DetailedFormDescription,
                              PricingAndInventoryForm, 
                              ImageAndMediaForm, 
                              ShippingAndDeliveryForm,
                              SeoAndMetaForm,
                              AdditionalInformationForm,
                              )


from .views_helpers import get_base64_images_from_session


# Create your views here.

@login_required
def account(request):
    return render(request, "account/account/account.html")


@login_required
def landing_page(request):
    return render(request, "account/account/landing_page.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def product_management(request):
    return render(request, "account/product-management/add-new-product/product-management-overview.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_basic_description(request):
    
    return handle_form(
        request=request,
        form_class=BasicFormDescription,
        session_key='basic_form_description',
        next_url_name='detailed_description_form',
        template_name='account/product-management/add-new-product/basic-product-information.html',
      
    )

@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_detailed_description(request):
    return handle_form(
        request=request,
        form_class=DetailedFormDescription,
        session_key='detailed_form_description',
        next_url_name='pricing_and_inventory_form',
        template_name='account/product-management/add-new-product/detailed-description-specs.html',
        checkbox_fields_to_store=("size", "color")
    )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_pricing_and_inventory(request):
     return handle_form(
        request=request,
        form_class=PricingAndInventoryForm,
        session_key='pricing_and_inventory_form',
        next_url_name='images_and_media_form',
        template_name='account/product-management/add-new-product/pricing-inventory.html'
    )
   

@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
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
                        temp_file_paths[field]  = save_file_temporarily(request.FILES[field])
                request.session["temp_file_paths"] = temp_file_paths
                
            return redirect(reverse("shipping_and_delivery_form"))
    
    context["form"] = form
    return render(request, "account/product-management/add-new-product/images-and-media.html", context=context)


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_shipping_and_delivery(request):
    return handle_form(request=request,
                       form_class=ShippingAndDeliveryForm,
                       session_key="shipping_and_delivery",
                       next_url_name="seo_and_meta_form",
                       template_name="account/product-management/add-new-product/shipping-and-delivery.html",
                       checkbox_fields_to_store=("shipping",)
                       )



@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_seo_management(request):
    return handle_form(request=request,
                       form_class=SeoAndMetaForm,
                       session_key="seo_management",
                       next_url_name="add_information_form",
                       template_name="account/product-management/add-new-product/SEO-and-meta-information.html",
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_additonal_information(request):
    return handle_form(request=request,
                       form_class=AdditionalInformationForm,
                       session_key="additional_information",
                       next_url_name="view_review",
                       template_name="account/product-management/add-new-product/additonal-information.html",
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def view_review(request):
    context = { "section_id" : "review-section", 'is_review_section': True}
    
    image_and_media_session = request.session.get("temp_file_paths", {})
  
    # add to the context
    context["basic_form_data"]             = request.session.get("basic_form_description", {})
    context["detailed_form_data"]          = request.session.get("detailed_form_description", {})
    context["price_and_inventory_data"]    = request.session.get("pricing_and_inventory_form", {})
    context["image_and_media_data"]        = get_base64_images_from_session(image_and_media_session)
    context["shipping_and_delivery_data"]  = request.session.get("shipping_and_delivery", {})
    context["seo_management_data"]         = request.session.get("seo_management", {})
    context["additional_information_data"] = request.session.get("additional_information", {})   
    
    print(context["shipping_and_delivery_data"])
    return render(request, "account/product-management/add-new-product/review-and-submit.html", context=context)
 
 
 
 
@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def view_products(request):
    return render(request, "account/product-management/view-products/view-products.html")
 

@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def orders(request):
    return render(request, "account/orders/orders.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def view_item(request, id):
    return render(request, "account/orders/view-item.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def financial_management(request):
    return render(request, "account/financial-management/financial-management.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def invoice(request, item_id):
    return render(request, "account/orders/invoice.html" )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def refund_overview(request):
    return render(request, "account/refund/refund-management.html")

