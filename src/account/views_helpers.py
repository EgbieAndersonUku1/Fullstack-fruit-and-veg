from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from typing import List

from .utils.utils import create_timestamped_directory, get_saved_temp_file,  upload_to
from utils.converter import encode_image_bytes_to_base64, convert_decimal_to_float
from product.models import Product, Category, Brand, ProductVariation, Shipping
from utils.converter import decode_base64_to_image_bytes
from utils.generator import generate_random_image_filename


def handle_form(request, form_class, session_key, next_url_name, template_name, checkbox_fields_to_store=set()):
    """
    Handles form processing, session management, and checkbox state preservation.

    This function initializes and processes a form, validates the submitted data, 
    and manages the storage of form data in the session. It also handles the storage 
    of selected checkbox values for specific input fields in the session, allowing 
    the state of these checkboxes to be preserved across form submissions.

    Parameters:
        - request: HttpRequest object containing metadata about the request.
        - form_class: The form class to instantiate and process.
        - session_key: The key used to store and retrieve the form data from the session.
        - next_url_name: The name of the URL to redirect to after a successful form submission.
        - template_name: The name of the template to render if the form is not valid or if the form is initially loaded.
        - checkbox_fields_to_store: (Optional) A set of input field names (strings) that correspond to groups of 
        checkboxes. The selected values for these checkboxes will be stored in the session under keys 
        matching the input field names. If a single input field name is entered it must 
        followed by a comma, e.g ("color", ). Note: This only applies to a single field name
        
        

    Returns:
        - HttpResponse: Redirects to the URL specified by `next_url_name` if the form is successfully 
        submitted and valid; otherwise, renders the specified template with the form.

    Additional Functionality:
        - Stores the checked states of specified checkbox groups in the session, using the names provided 
        in `checkbox_fields_to_store`. These states are then used to pre-populate the form when it is rendered.

        Example HTML Usage:
        -------------------
        To use `checkbox_fields_to_store`, you might create a form like the following:

        <form method="POST" action="{% url 'form_view_url_name' %}">
            {% csrf_token %}

            <!-- Checkbox group for colors -->
            <div>
                <label>Choose your favorite colors:</label><br>
                <div>
                    <input type="checkbox" id="color_red" name="color" value="red"
                    <label for="color_red">Red</label>
                </div>
                <div>
                    <input type="checkbox" id="color_blue" name="color" value="blue"
                    <label for="color_blue">Blue</label>
                </div>
        
            </div>

            <!-- Checkbox group for foods -->
            <div>
                <label>Choose your favorite foods:</label><br>
                <div>
                    <input type="checkbox" id="food_pizza" name="food" value="pizza"
                    <label for="food_pizza">Pizza</label>
                </div>
                <div>
                    <input type="checkbox" id="food_sushi" name="food" value="sushi"
                    <label for="food_sushi">Sushi</label>
                </div>
               
            </div>

            <!-- Add other checkbox groups as needed, e.g., size, numbers, etc. -->

            <button type="submit">Submit</button>
        </form>

        In this example:
        - `checkbox_fields_to_store` would be passed as `("color", "food")` where this is the value associated with name.
        - The selected values for the `color` and `food` checkboxes will be stored in the session.
        - When the form is re-rendered, these values will be pre-checked based on the session data.
    """
  
    initial_data = request.session.get(session_key, {})
 
   
    form = form_class(initial=initial_data)
    context = {"section_id": session_key}
    stored_checked_inputs_to_context(request, session_key, checkbox_fields_to_store, context)
    
    if request.method == "POST":
        
        form = form_class(request.POST)
        if form.is_valid():
            if form.has_changed():
                request.session[session_key] = convert_decimal_to_float(form.cleaned_data)
               
                store_checked_inputs_in_session(request, checkbox_fields_to_store, session_key)
                            
            return redirect(reverse(next_url_name))
    
    context["form"] = form
    
    return render(request, template_name, context=context)



def store_checked_inputs_in_session(request, checkbox_elements, session_key):
    
    if (not checkbox_elements):
        return
    
    for element_name in checkbox_elements:
        
        values = request.POST.getlist(element_name)
        if values:
            
            # change each value to a capital before storing it in the session
            request.session[session_key][element_name] = [value.title() for value in values] 
    
    


def stored_checked_inputs_to_context(request, session_key, check_box_fields, context):
    """
    Populates the context dictionary with values of checked input fields 
    that are stored in the session.

    This function checks if there are stored values for specific checkbox fields 
    in the session using a given session key. If these values exist, they are 
    added to the context dictionary to maintain the state of the checkboxes 
    across requests.

    Args:
        request (HttpRequest): The HTTP request object, which contains the session data.
        session_key (str): The key used to retrieve the stored checkbox data from the session.
        check_box_fields (set of str): A set of field names representing the checkbox inputs 
                                        that need to be checked for stored values.
        context (dict): The context dictionary to be populated with the stored checkbox values.
    """
    if request.session.get(session_key):
        for field_name in check_box_fields:
            try:
                context[field_name] = request.session[session_key][field_name]
            except KeyError:
                pass

    
def save_file_with_timestamped_directory(file, base_folder, create_unique_name_func):
    """
    Save a file to a timestamped directory with a unique file name.

    Args:
        file (File): The file object to be saved.
        base_folder (str): The base folder where the file should be saved.
        create_unique_name_func (function): A function that takes the original file name and returns a unique file name.

    Returns:
        pathlib.Path: A `Path` object representing the full path of the saved file.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: For any other errors that may occur during the process.
    """

    # Check if the file exists before processing
    if not file or not hasattr(file, 'name'):
        raise FileNotFoundError("The file was not found or is invalid.")

    try:
       
        unique_file_name = create_unique_name_func(file.name)
    except Exception as e:
        raise Exception(f"An error occurred while generating a unique file name: {e}")

    file_path = create_timestamped_directory(base_folder)
    full_file_path = file_path / unique_file_name

   
    try:
        upload_to(file=file, destination_folder=full_file_path)
    except Exception as e:
        raise Exception(f"An error occurred while uploading the file: {e}")

    return full_file_path





def get_base64_images_from_session(session_dict):
    """
    Retrieve and encode images from a session dictionary in Base64 format.

    Args:
        session_dict (dict): A dictionary where keys are image names and values are file paths.

    Returns:
        list: A list of Base64 encoded image strings.

    Raises:
        ValueError: If the session_dict is empty.
        TypeError: If session_dict is not a dictionary.
        FileNotFoundError: If a file path is invalid.
    """
    images = []

   
    if not session_dict:
        raise ValueError("The session dictionary cannot be empty.")
    
    if not isinstance(session_dict, dict):
        raise TypeError("The session dictionary should be a dictionary.")
    
   
    for _, file_path in session_dict.items():
        try:
            image_bytes = get_saved_temp_file(file_path)
            if image_bytes:
                encoded_image = encode_image_bytes_to_base64(image_bytes)
                images.append(encoded_image)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    return images



 
def get_category(context):
    
    NOT_APPLICABLE  = "N/A"

    category_name  = context.get("new_category", NOT_APPLICABLE)
    if category_name == NOT_APPLICABLE:
        category_name = context.get("category")
    
    if not category_name:
        raise ValueError("Expected a category name but got None")
    return category_name
    
    
    
def save_images(images):
    BASE_FOLDER = "product_images"
    
    # Extract images from the context (base64 to image byte objects)
    if len(images) != 3:
        raise ValueError("Expected three images, but received a different number.")
    
    main_image, side_image_1, side_image_2 = extract_images(images)
    
    # Save images to storage and return paths
    fs = FileSystemStorage()
    
    main_image_path   = save_image_to_storage(main_image,   "main_image", BASE_FOLDER, fs)
    side_image_1_path = save_image_to_storage(side_image_1, "side_image", BASE_FOLDER, fs)
    side_image_2_path = save_image_to_storage(side_image_2, "side_image", BASE_FOLDER, fs)
    
    return main_image_path, side_image_1_path, side_image_2_path


def extract_images(images):
    # Make sure we have exactly three images to decode
    
    try:
        main_image   = decode_base64_to_image_bytes(images[0])
        side_image_1 = decode_base64_to_image_bytes(images[1])
        side_image_2 = decode_base64_to_image_bytes(images[2])
        return main_image, side_image_1, side_image_2
    except Exception as e:
        raise ValueError(f"Error decoding images: {str(e)}")


def save_image_to_storage(image, image_type, folder, fs):
    # Generate a random filename and save the image to storage
    filename = generate_random_image_filename(image_type, image, folder)
    image_path = fs.save(filename, image)
    return image_path




def create_product_variations(product, merged_context) -> List[ProductVariation]:
    """
    Create product variations based on size and color combinations from the merged context.

    :param product: A Product instance.
    :param merged_context: A dictionary containing size, color, and other product details.
    :return: A list of ProductVariation instances.
    """
    if not isinstance(product, Product):
        raise ValueError(
            f"The product instance is not of type Product. Expected Product instance, got {type(product).__name__}."
        )

    # Required keys for ProductVariation creation
    required_keys = [
        "sizes",
        "colors",
        "height",
        "width",
        "length",
        "available",
        "quantity_stock",
        "minimum_order",
        "maximum_order",
    ]

    # Validate required keys
    missing_keys = [key for key in required_keys if key not in merged_context]
    if missing_keys:
        raise KeyError(f"The following keys are missing in merged_context: {', '.join(missing_keys)}")

    product_variations = []

    # Iterate over size and color combinations to create ProductVariation instances
    for size in merged_context.get("sizes", []):
        for color in merged_context.get("colors", []):
            product_variations.append(
                ProductVariation(
                    product=product,
                    color=color,
                    size=size,
                    height=merged_context["height"],
                    width=merged_context["width"],
                    length=merged_context["length"],
                    availability=merged_context["available"],
                    stock_quantity=merged_context["quantity_stock"],
                    minimum_stock_order=merged_context["minimum_order"],
                    maximum_stock_order=merged_context["maximum_order"],
                )
            )

    return product_variations


def create_shipping_variations(product, merged_context) -> List[Shipping]:
    """
    Create shipping variations for a given product based on delivery options in the merged context.

    :param product: A Product instance.
    :param merged_context: A dictionary containing shipping details and options.
    :return: A list of Shipping instances.
    """
    if not isinstance(product, Product):
        raise ValueError(
            f"The product instance is not of type Product. Expected Product instance, got {type(product).__name__}."
        )

    # Required keys for Shipping object creation
    required_keys = [
        "delivery_options",
        "shipping_height",
        "shipping_width",
        "shipping_length",
        "shipping_weight",
    ]
    
    # Validate required keys
    missing_keys = [key for key in required_keys if key not in merged_context]
    if missing_keys:
        raise KeyError(f"The following keys are missing in merged_context: {', '.join(missing_keys)}")

    delivery_variations = []

    for delivery_option in merged_context.get("delivery_options", []):
        price = 0  
        if delivery_option == Shipping.ShippingType.STANDARD:
            price = merged_context.get("standard_shipping", 0)
        elif delivery_option == Shipping.ShippingType.PREMIUM:
            price = merged_context.get("premium_shipping", 0)
        elif delivery_option == Shipping.ShippingType.EXPRESS:
            price = merged_context.get("express_shipping", 0)

        # Append the created Shipping instance
        delivery_variations.append(
            Shipping(
                product=product,
                height=merged_context["shipping_height"],
                width=merged_context["shipping_width"],
                length=merged_context["shipping_length"],
                weight=merged_context["shipping_weight"],
                price=price,
                shipping_type=delivery_option,
            )
        )

    return delivery_variations
