import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
from .forms.user_profile_form import (UserProfileForm, 
                                      BillingAddressForm, 
                                      ShippingAddressForm,
                                      PrimaryAddress
                                      )
from .models import BillingAddress, ShippingAddress


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
                return redirect("user_profile")
        
    context = {
        "user_profile_form": user_profile_form,
        "billing_address_form": billing_address_form,
        "shipping_address_form": shipping_address_form,
    }
    
    return render(request, "user_profile/user_profile.html", context=context)




def manage_billing_addresses(request):
    
    profile            = request.user.profile
    billing_addresses  = BillingAddress.objects.filter(user_profile=profile)
    primary_address    = billing_addresses.filter(primary_address=True).first()  
  
    billing_address_minus_primary_address = billing_addresses.exclude(primary_address=True)
    context = {
        "billing_addresses": billing_address_minus_primary_address.all(),
        "primary_address": primary_address,
        "REMAINING_BILLING_COUNT": billing_address_minus_primary_address.count(), 
    }
    
    return render(request, "profile/manage_billing_addresses.html", context)


def manage_shippng_addresses(request):
    profile            = request.user.profile
    shipping_addresses = ShippingAddress.objects.filter(user_profile=profile) 
  
    context = {
        "shipping_addresses": shipping_addresses.all(),
        "REMAINING_SHIPPING_COUNT": shipping_addresses.count(),
    }
    
    return render(request, "profile/manage_shipping_addresses.html", context)

    
def delete_address(request):
  
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            if not data.get("_method") == "DELETE":
                raise ValueError("This is not a delete request")
            
            is_billing_address = data.get("is_billing_address")
            address_id         = data.get("address_id")
            
        except json.JSONDecodeError:
            return JsonResponse({"SUCCESS": False, "MESSAGE": "Invalid request"}, status=400)

        user_profile = request.user.profile

        if is_billing_address:
            deleted_count, _ = BillingAddress.objects.filter(user_profile=user_profile, id=address_id).delete()
          
        else:
            deleted_count, _ = ShippingAddress.objects.filter(user_profile=user_profile, id=address_id).delete()
            

        if deleted_count >= 0:
            remaining_shipping_count = ShippingAddress.objects.filter(user_profile=user_profile).count()
            remaining_billing_count  = BillingAddress.objects.filter(user_profile=user_profile).count()
            
            return JsonResponse({"SUCCESS": True, 
                                  "MESSAGE": "Address deleted successfully",
                                  "REMAINING_SHIPPING_COUNT": remaining_shipping_count,
                                  "REMAINING_BILLING_COUNT": remaining_billing_count,
                                  }, status=200)

        return JsonResponse({"SUCCESS": False, "MESSAGE": "Address not found"}, status=404)

    return JsonResponse({"SUCCESS": False, "MESSAGE": "Method Not Allowed"}, status=405)


def mark_as_primary_address(request, id):
    is_shipping_address = request.POST.get("is_shipping_address")
    pass