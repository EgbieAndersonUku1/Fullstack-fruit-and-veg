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


def orders(request):
    return render(request, "account/orders/orders.html")


def view_item(request, id):
    return render(request, "account/orders/view-item.html")


def financial_management(request):
    return render(request, "account/financial-management/financial-management.html")



def invoice(request, item_id):
    return render(request, "account/orders/invoice.html" )