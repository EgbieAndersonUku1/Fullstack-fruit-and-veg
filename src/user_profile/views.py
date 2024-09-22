from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.
from .forms.user_profile_form import UserProfileForm, BillingAddressForm, ShippingAddressForm, PrimaryAddress


def user_profile(request):
   
    user_profile_form     = UserProfileForm(instance=request.user.profile)
    billing_address_form  = BillingAddressForm(prefix="billing_address_form")
    shipping_address_form = ShippingAddressForm(prefix="shipping_address_form")
    
     
    if request.method == "POST":
      
        user_profile_form     = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        billing_address_form  = BillingAddressForm(request.POST, prefix="billing_address_form")
        shipping_address_form = ShippingAddressForm(request.POST, prefix="shipping_address_form")
       
        is_billing_address_same_as_shipping = request.POST.get("billing_address_is_shipping")
        should_redirect = False
        
        if user_profile_form.is_valid():
            user_profile = user_profile_form.save()
            
            
            if billing_address_form.is_valid():
                billing_address = billing_address_form.save(commit=False)  
                
                if billing_address_form.cleaned_data["is_primary_address"] ==  PrimaryAddress.YES:
                    billing_address.mark_as_primary(save=False)
                
                billing_address.user_profile = user_profile
                billing_address.save()
                should_redirect = True
                
            # Optional shipping address save based on user selection in the front UI
            if is_billing_address_same_as_shipping == "no" and shipping_address_form.is_valid():
                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.user_profile = user_profile
                shipping_address.save()
            
            if should_redirect:
                messages.success(request, "You have successfully updated your profile page")
                return redirect("account")
        
    context = {
        "user_profile_form": user_profile_form,
        "billing_address_form": billing_address_form,
        "shipping_address_form": shipping_address_form,
    }
    
    return render(request, "user_profile/user_profile.html", context=context)
