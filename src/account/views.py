from django.shortcuts import render

# Create your views here.



def account(request):
    return render(request, "account/account/account.html")


def product_management(request):
    return render(request, "account/product-management/add-new-product/product-management-overview.html")


def add_basic_description(request):
    return render(request, "account/product-management/add-new-product/basic-product-information.html")


def add_detailed_description(request):
    return render(request, "account/product-management/add-new-product/detailed-descripton-specs.html")
