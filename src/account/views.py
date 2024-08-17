from django.shortcuts import render

from .forms import BasicFormDescription

# Create your views here.


def account(request):
    return render(request, "account/account/account.html")


def product_management(request):
    return render(request, "account/product-management/add-new-product/product-management-overview.html")


def add_basic_description(request):
    
    form    = BasicFormDescription()
    context = {"section_id" : "basic-description"}
    
    if (request.method == "POST"):
        form = BasicFormDescription(request.POST)
        if form.is_valid():
            # Do nothing for now logic will be added later
            pass
    
    context["form"] = form
    return render(request, "account/product-management/add-new-product/basic-product-information.html", context=context)


def add_detailed_description(request):
    context = {
        "section_id" : "detailed_descritpion",
    }
    return render(request, "account/product-management/add-new-product/detailed-description-specs.html", context=context)


def add_pricing_and_inventory(request):
    context = {
        "section_id" : "pricing-and-inventory",
    }
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