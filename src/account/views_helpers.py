from django.shortcuts import render, redirect
from django.urls import reverse
from pathlib import Path
from time import time
from django.utils import timezone

from .utils.utils import create_timestamped_directory,  upload_to

from account.utils.converter import convert_decimal_to_float




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
        matching the input field names.

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

    if request.method == "POST":
        
        form = form_class(request.POST)
        if form.is_valid():
            if form.has_changed():
                request.session[session_key] = convert_decimal_to_float(form.cleaned_data)
                
                store_checked_inputs_in_session(request, checkbox_fields_to_store)
                            
            return redirect(reverse(next_url_name))
    
    context["form"] = form
    return render(request, template_name, context=context)



def store_checked_inputs_in_session(request, checkbox_elements):
    
    if (not checkbox_elements):
        return
    
    for value in checkbox_elements:
        request.session[value] = request.POST.getlist(value)
    
    
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





