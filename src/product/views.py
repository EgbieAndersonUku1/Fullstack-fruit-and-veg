from django.shortcuts import render

# Create your views here.


def product_details(request):
    return render(request, "account/product-management/view-products/product_detailed_page.html")