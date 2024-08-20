from django.shortcuts import render, redirect
from django.urls import reverse
from pathlib import Path
from time import time
from django.utils import timezone

from .utils.utils import create_timestamped_directory,  upload_to

from account.utils.converter import convert_decimal_to_float


def handle_form(request, form_class, session_key, next_url_name, template_name):
    initial_data = request.session.get(session_key, {})
    form = form_class(initial=initial_data)
    context = {"section_id": session_key}

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            if form.has_changed():
                request.session[session_key] = convert_decimal_to_float(form.cleaned_data)
            return redirect(reverse(next_url_name))
    
    context["form"] = form
    return render(request, template_name, context=context)


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





