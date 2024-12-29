from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.


def product_details(request):
    
    context = {
        "logged_in": request.user.is_authenticated,
    }
    
    return render(request, 
                  "account/product-management/view-products/product_detailed_page.html",
                  context=context)