import base64

from os.path import splitext, join
import tempfile

from pathlib import Path
from time import time
from django.utils import timezone



def upload_to(file, destination_folder):
    
    with open(destination_folder, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
            

def save_file_temporarily(uploaded_file):
    """
    Save the uploaded file temporarily using a local temporary directory.
    """
    
    temp_dir       = tempfile.mkdtemp()
    temp_file_path = join(temp_dir, uploaded_file.name)
    
    with open(temp_file_path, 'wb+') as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
    
    return temp_file_path


def get_saved_temp_file(temp_file_path):
    with open(temp_file_path, 'rb') as file:
        file_bytes = file.read()
        return file_bytes


def encode_image_bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')
    

def create_unique_file_name(original_name):
    
    name, ext     = splitext(original_name)
    timestamp     = time()
    new_file_name = f"{name}_{timestamp}.{ext}"
    return new_file_name



def create_timestamped_directory(folder_name):
    """
    Create a directory path that includes a timestamp based on the current date.

    This function generates a directory structure by combining the specified base folder name
    with the current year, month, and day. The directory is created if it does not already exist,
    ensuring that files can be organized by date.

    Args:
        folder_name (str): The base folder name where the directory structure should be created.

    Returns:
        pathlib.Path: A `Path` object representing the created directory path.

    Raises:
        FileNotFoundError: If the directory cannot be created.

    Example:
        >>> create_timestamped_directory('uploads/images')
        PosixPath('uploads/images/2024/8/20')

    Note:
        - The `folder_name` should be a base directory that exists or is intended to be created.
        - The function uses Django's `timezone.now()` to ensure the timestamp reflects the current date
          and time in the server's timezone.
    """
    today = timezone.now()
    path = Path(folder_name) / str(today.year) / str(today.month) / str(today.day)
    
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise FileNotFoundError(f"Failed to create directory: {e}")
    
    return path
    
