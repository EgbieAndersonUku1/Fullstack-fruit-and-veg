from django.shortcuts                import render, redirect
from django.urls                     import reverse
from django.conf                     import settings
from django.contrib.auth.decorators  import login_required
from django.contrib                  import messages

from account.utils.utils  import save_file_temporarily
from utils.custom_errors  import EmptyProductFormError, EmptyMediaAndImagesError


from .views_helpers import (get_base64_images_from_session, 
                            handle_form,
                            save_images,
                            get_category,
                            create_product_variations,
                            create_shipping_variations,
                            redirect_to_incomplete_step,
                            clear_product_request,
                            )

from .forms.forms   import (  BasicFormDescription, 
                              DetailedFormDescription,
                              PricingAndInventoryForm, 
                              ImageAndMediaForm, 
                              ShippingAndDeliveryForm,
                              SeoAndMetaForm,
                              NutritionForm,
                              AdditionalInformationForm,
                              )

from product.models import Product, Category, Brand, Shipping, ProductVariation, Manufacturer


# Create your views here.

@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def account(request):
    return render(request, "account/account/account.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
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
        current_step=1,
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
        current_step=2,
        checkbox_fields_to_store=("size", "color")
    )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_pricing_and_inventory(request):
     return handle_form(
        request=request,
        form_class=PricingAndInventoryForm,
        session_key='pricing_and_inventory_form',
        next_url_name='images_and_media_form',
        template_name='account/product-management/add-new-product/pricing-inventory.html',
        current_step=3,
    )
   

@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_images_and_media(request):
    
    context      = {"section_id" : "images-and-media"}
    initial_data = request.session.get("temp_file_paths", {})
    form         = ImageAndMediaForm(initial=initial_data)
    
    
    if request.method == "POST":
        
        form = ImageAndMediaForm(request.POST, request.FILES)
        if form.is_valid():
            request.session["step4_completed"]  = True
            if form.has_changed():
                
                file_fields     = ['primary_image', 'side_image1', 'side_image2', 'primary_video']
                temp_file_paths = {}
                
                for field in file_fields:
                    if field in request.FILES:
                        temp_file_paths[field]     = save_file_temporarily(request.FILES[field])
                request.session["temp_file_paths"]  = temp_file_paths
              
                
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
                       checkbox_fields_to_store=("shipping",),
                       current_step=5,
                       )



@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_seo_management(request):
    return handle_form(request=request,
                       form_class=SeoAndMetaForm,
                       session_key="seo_management",
                       next_url_name="nutrition_form",
                       template_name="account/product-management/add-new-product/SEO-and-meta-information.html",
                       current_step=6
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_nutrition(request):
    return handle_form(request=request,
                       form_class=NutritionForm,
                       session_key="nutrition",
                       next_url_name="add_information_form",
                       template_name="account/product-management/add-new-product/nutrition.html",
                       current_step=7,
                       
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_additonal_information(request):
    return handle_form(request=request,
                       form_class=AdditionalInformationForm,
                       session_key="additional_information",
                       next_url_name="view_review",
                       template_name="account/product-management/add-new-product/additonal-information.html",
                       current_step=8
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def view_review(request):
    
    context = { "section_id" : "review-section", 'is_review_section': True}
    
    image_and_media_session = request.session.get("temp_file_paths", {})
    
    # show in the review section through the context
    context["basic_form_data"]             = request.session.get("basic_form_description", {})
    context["detailed_form_data"]          = request.session.get("detailed_form_description", {})
    context["price_and_inventory_data"]    = request.session.get("pricing_and_inventory_form", {})
 
    context["shipping_and_delivery_data"]  = request.session.get("shipping_and_delivery", {})
    context["seo_management_data"]         = request.session.get("seo_management", {})
    context["nutrition_data"]              = request.session.get("nutrition", {})        
    context["additional_information_data"] = request.session.get("additional_information", {}) 
    
    try:
        context["image_and_media_data"] = get_base64_images_from_session(image_and_media_session)
    except ValueError as e:
        print(e)
        messages.error(request, "Something went wrong and your images couldn't be found. Please upload again and then submit again")
        # return redirect(reverse("images_and_media_form"))
    
    return redirect_to_incomplete_step(request, "account/product-management/add-new-product/review-and-submit.html", context=context)
 
 
 
@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def process_and_save_product_form(request):
    
    merged_context = {
        **request.session.get("basic_form_description", {}),
        **request.session.get("detailed_form_description", {}),
        **request.session.get("pricing_and_inventory_form", {}),
        **request.session.get("shipping_and_delivery", {}),
        **request.session.get("seo_management", {}),
        **request.session.get("nutrition", {}),        
        **request.session.get("additional_information", {}) 
    
    }
    
    if not merged_context:
        raise EmptyProductFormError("No data was provided in the product form. Please ensure all required fields are filled.")

    image_and_media_session = request.session.get("temp_file_paths", {})
    
    if not image_and_media_session:
        raise EmptyMediaAndImagesError("No images were found. Please ensure that there are images associated with this product")
    
    
    images = get_base64_images_from_session(image_and_media_session)
    
    main_image_path, side_image_1_path, side_image_2_path = save_images(images)
    
    is_featured   = True  if merged_context.get("is_featured_item", "").lower() == "y"   else False
    is_discounted = True  if merged_context.get("select_discount", "").lower()  == "yes" else False
    is_returnable = True  if merged_context.get("return_policy", "").lower()    == "y"   else False
    
    category, _  = Category.objects.get_or_create(category=get_category(merged_context))
    brand,    _  = Brand.objects.get_or_create(name=merged_context.get("brand"))
    
    manufactuer, _ = Manufacturer.objects.get_or_create(
        name=merged_context.get("manufacturer"),
        description=merged_context.get("manufacturer_description"),
        address=merged_context.get("manufacturer_address"),
        contact_num=merged_context.get("manufacturer_phone_number"),
    )
    
    manufactuer.save()
   
    product = Product(
        name=merged_context.get("name"),
        is_featured=is_featured,
        long_description=merged_context.get("description"),
        short_description=merged_context.get("short_description"),
        category=category,
        brand=brand,
        sku=merged_context.get("sku"),
        upc=merged_context.get("upc"),
        price=merged_context.get("price"),
        weight=merged_context.get("weight"),
        is_discounted_price=is_discounted,
        discount_price=merged_context.get("add_discount"), 
        primary_image=main_image_path,
        side_image=side_image_1_path,
        side_image_2=side_image_2_path,
        meta_title=merged_context.get("meta_title"),
        meta_keywords=merged_context.get("meta_keywords"),
        meta_description=merged_context.get("meta_description"),
        manufacturer=manufactuer,
        is_returnable=is_returnable,
        recommendation=merged_context.get("recommendation"),
        country_of_origin=merged_context.get("country_made"),
        warranty_period=merged_context.get("warranty_description"),
        nutrition={
            'calories': merged_context.get("calories"), 
            'carbohydrates': merged_context.get("carbohydrates"), 
            'sugar': merged_context.get("sugar"),
            'protein': merged_context.get("protein"),
            'fibre': merged_context.get("fibre"),   
        }
        
    )
    
    product.save()
    product_variations_list     = create_product_variations(product, merged_context)
    product_shipping_variations = create_shipping_variations(product, merged_context)
    
    # Batch save for efficiency 
    ProductVariation.objects.bulk_create(product_variations_list)  
    Shipping.objects.bulk_create(product_shipping_variations)
    
    clear_product_request(request)
    
    messages.success(request, "You have successfully added the product to the database")
    return redirect(reverse("basic_description_form"))
 
  
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

