from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BasicFormDescription, DetailedFormDescription, PricingAndInventoryForm

from .utils.converter import convert_decimal_to_float

# Create your views here.


def account(request):
    return render(request, "account/account/account.html")


def product_management(request):
    return render(request, "account/product-management/add-new-product/product-management-overview.html")


def add_basic_description(request):
    
    initial_data = request.session.get('basic_form_description', {})
    
  
    form    = BasicFormDescription(initial=initial_data) # Prepopulate the form with the session data
    context = {"section_id" : "basic-description"}
    
    if (request.method == "POST"):
        form = BasicFormDescription(request.POST)
        if form.is_valid():
           
            if form.has_changed():
                 request.session["basic_form_description"] = form.cleaned_data
            return redirect(reverse("detailed_description_form"))
    
    context["form"] = form
    return render(request, "account/product-management/add-new-product/basic-product-information.html", context=context)


def add_detailed_description(request):
    
    initial_data = request.session.get('detailed_form_description', {})
    context      = {"section_id" : "detailed_description"}
    form         = DetailedFormDescription(initial=initial_data) # Prepopulate the form with the session data

    
    if (request.method == "POST"):
        
        form = DetailedFormDescription(request.POST)
        if form.is_valid():
          
            if form.has_changed():
                request.session["detailed_form_description"] = convert_decimal_to_float(form.cleaned_data)
                request.session["selected_colors"]           = request.POST.getlist('color')
                request.session["selected_sizes"]            = request.POST.getlist("size")
            
            return redirect(reverse("pricing_and_inventory_form"))
    
    context["form"] = form
    return render(request, "account/product-management/add-new-product/detailed-description-specs.html", context=context)


def add_pricing_and_inventory(request):
    
    initial_data = request.session.get("pricing_and_inventory_form", {})
    context      = { "section_id" : "pricing-and-inventory"}
    form         = PricingAndInventoryForm(initial=initial_data) # Prepopulate the form with the session data
    
    if (request.method == "POST"):
        
        form = PricingAndInventoryForm(request.POST)
      
        if form.is_valid():
            if form.has_changed():
                  request.session["pricing_and_inventory_form"] = convert_decimal_to_float(form.cleaned_data)
            return redirect(reverse("images_and_media_form"))
                

    context["form"] = form
   
    return render(request, "account/product-management/add-new-product/pricing-inventory.html", context=context)


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