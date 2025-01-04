from django.shortcuts                import render, redirect
from django.core.files.storage       import FileSystemStorage
from django.urls                     import reverse
from django.conf                     import settings
from django.contrib.auth.decorators  import login_required

from account.utils.utils             import save_file_temporarily
from authentication.forms.login_form import LoginForm

from .views_helpers import handle_form
from .forms.forms   import (  BasicFormDescription, 
                              DetailedFormDescription,
                              PricingAndInventoryForm, 
                              ImageAndMediaForm, 
                              ShippingAndDeliveryForm,
                              SeoAndMetaForm,
                              NutritionForm,
                              AdditionalInformationForm,
                              )

from product.models import Product, Category, Brand, ProductVariation

from .views_helpers import get_base64_images_from_session
from utils.converter import decode_base64_to_image_bytes
from utils.generator import generate_random_image_filename



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
        checkbox_fields_to_store=("size", "color")
    )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_pricing_and_inventory(request):
     return handle_form(
        request=request,
        form_class=PricingAndInventoryForm,
        session_key='pricing_and_inventory_form',
        next_url_name='images_and_media_form',
        template_name='account/product-management/add-new-product/pricing-inventory.html'
    )
   

@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_images_and_media(request):
    
    context      = {"section_id" : "images-and-media"}
    initial_data = request.session.get("temp_file_paths", {})
    form         = ImageAndMediaForm(initial=initial_data)
    
    if request.method == "POST":
        
        form = ImageAndMediaForm(request.POST, request.FILES)
        if form.is_valid():
    
            if form.has_changed():
                
                file_fields     = ['primary_image', 'side_image1', 'side_image2', 'primary_video']
                temp_file_paths = {}
                
                for field in file_fields:
                    if field in request.FILES:
                        temp_file_paths[field]  = save_file_temporarily(request.FILES[field])
                request.session["temp_file_paths"] = temp_file_paths
                
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
                       checkbox_fields_to_store=("shipping",)
                       )



@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_seo_management(request):
    return handle_form(request=request,
                       form_class=SeoAndMetaForm,
                       session_key="seo_management",
                       next_url_name="nutrition_form",
                       template_name="account/product-management/add-new-product/SEO-and-meta-information.html",
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_nutrition(request):
    return handle_form(request=request,
                       form_class=NutritionForm,
                       session_key="nutrition",
                       next_url_name="add_information_form",
                       template_name="account/product-management/add-new-product/nutrition.html",
                       
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_additonal_information(request):
    return handle_form(request=request,
                       form_class=AdditionalInformationForm,
                       session_key="additional_information",
                       next_url_name="view_review",
                       template_name="account/product-management/add-new-product/additonal-information.html",
                       )


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def view_review(request):
    context = { "section_id" : "review-section", 'is_review_section': True}
    
    image_and_media_session = request.session.get("temp_file_paths", {})
  
    context["basic_form_data"]             = request.session.get("basic_form_description", {})
    context["detailed_form_data"]          = request.session.get("detailed_form_description", {})
    context["price_and_inventory_data"]    = request.session.get("pricing_and_inventory_form", {})
    context["image_and_media_data"]        = get_base64_images_from_session(image_and_media_session)
    context["shipping_and_delivery_data"]  = request.session.get("shipping_and_delivery", {})
    context["seo_management_data"]         = request.session.get("seo_management", {})
    context["nutrition_data"]              = request.session.get("nutrition", {})        
    context["additional_information_data"] = request.session.get("additional_information", {})   
    
    # get the sizes and colors stored in as a dict within a list e.g {size: ["red", "blue"], color: ["purple", "green"]}
    product_variations = []
    sizes         = context["detailed_form_data"].get("size", [])
    colors        = context["detailed_form_data"].get("color", [])
    detailed_data = context["detailed_form_data"]
    
    # decode the image from temp folder
    BASE_FOLDER  = "product_images"
    images       = context["image_and_media_data"]
    main_image, side_image_1, side_image_2  = decode_base64_to_image_bytes(images[0]), decode_base64_to_image_bytes(images[1]), decode_base64_to_image_bytes(images[2])
    
  
    # # Save the images to the filesystem (this makes them permanent)
    fs = FileSystemStorage()
    
    main_image_filename   = generate_random_image_filename("main_image", main_image, BASE_FOLDER)
    side_image_1_filename = generate_random_image_filename("side_image", side_image_1, BASE_FOLDER)
    side_image_2_filename = generate_random_image_filename("side_image", side_image_2, BASE_FOLDER)
    
    main_image_path   = fs.save(main_image_filename, main_image)
    side_image_1_path = fs.save(side_image_1_filename, side_image_1)
    side_image_2_path = fs.save(side_image_2_filename, side_image_2)
    
    is_featured = True if context["basic_form_data"]["is_featured_item"].lower() == "y" else False
    
    # Determine the category
    category_name  = context["basic_form_data"].get("new_category", "N/A")
    if category_name == "N/A":
        category_name = context["basic_form_data"]["category"]
    
    
    # determine if a discount option is chosen
    discounted_price   = 0
    is_discounted      = False

    if context["price_and_inventory_data"].get('select_discount', '').lower() == "yes":
        discounted_price = context["price_and_inventory_data"].get("add_discount")
        is_discounted    = True
    
    # Get or create the Category and Brand
    category, _ = Category.objects.get_or_create(category=category_name)
    brand,    _ = Brand.objects.get_or_create(name=context["basic_form_data"]["brand"])
    

    
    # create a model
    product = Product(
        name=context["basic_form_data"].get("name"),
        is_featured=is_featured,
        category=category,
        brand=brand,
        sku=context["basic_form_data"].get("sku", ""),
        short_description=context["basic_form_data"].get("short_description", ""),
        primary_image=main_image_path,
        side_image=side_image_1_path,
        side_image_2=side_image_2_path,
        weight=detailed_data.get("weight"),
        long_description=detailed_data.get("description", ""),
        price=context["price_and_inventory_data"].get("price"),
        is_discounted_price=is_discounted,
        discount_price=discounted_price,
       
    )
    
    
    # note to self - uncomment bottom line once all values have been extracted from the form
    # product.save()
    
    
    # Create and save product variations
    for size in sizes:
        for color in colors:
            product_variations.append(
                ProductVariation(
                    product=product,
                    color=color,
                    size=size,
                    height=detailed_data.get("height"),
                    width=detailed_data.get("width"),
                    length=detailed_data.get("length"),
                    availability=context["price_and_inventory_data"].get("available"),
                    stock_quantity=context["price_and_inventory_data"].get("quantity_stock"),
                    minimum_stock_order=context["price_and_inventory_data"].get("minimum_order"),
                    maximum_stock_order=context["price_and_inventory_data"].get("maximum_order"),
                    
                )
            )
    
    # note to self uncomment this to batch save after model is built
    # ProductVariation.objects.bulk_create(product_variations)  # Batch save for efficiency 
         
 
    return render(request, "account/product-management/add-new-product/review-and-submit.html", context=context)
 
 
 
 
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

