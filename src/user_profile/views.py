from django.shortcuts import render


# Create your views here.
from .forms.user_profile_form import UserProfileForm, BillingAddressForm, ShippingAddressForm
from .models import UserProfile


def user_profile(request):
    
    context               = {}
    form                  = UserProfileForm()
    billing_address_form  = BillingAddressForm()
    shipping_address_form = ShippingAddressForm()
    
    
    if request.method == "POST":
        
        form                  = UserProfileForm(request.POST)
        billing_address_form  = BillingAddressForm(request.POST)
        shipping_address_form = ShippingAddressForm(request.POST)
        
      
        if form.is_valid() and shipping_address_form.is_valid():
            
            profile               = form.save(commit=False)   
            billing_address_form  = billing_address_form.save(commit=False)
            shipping_address_form = shipping_address_form.save(commit=False)
            
            print("Saved")
            print("I should be here")
        else:
            print("Not valid")
            print("I shouldn't be here")
            # print(form.cleaned_data)
            # print(billing_address_form.cleaned_data)
            print(shipping_address_form.cleaned_data)
          
    context["form"]                  = form
    context["billing_address_form"]  = billing_address_form
    context["shipping_address_form"] = shipping_address_form
    context["user"]                  = request.user
    
    return render(request, "user_profile/user_profile.html", context=context)