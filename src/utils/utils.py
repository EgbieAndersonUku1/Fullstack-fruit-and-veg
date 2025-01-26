from django.http import HttpRequest
from PIL import Image
from socket import gethostname, gethostbyname

from device_detector import DeviceDetector

import requests
import hmac
import hashlib


def get_image_extenstion(image: Image) -> str:  
    """
    Takes an PIL image and returns the extenstion in lowercase.
    
    Args:
        Image: The PIL Image that will be used to extract the format.
        
    Returns:
        Returns the format if found or returns an empty string if not found.
    """  
    try:
        image = Image.open(image)
        return image.format.lower()
    except ValueError:
        return ''


def get_local_ip_address() -> str:
    """
    Returns the local IP address of the machine, not the global IP address.
    
    The local IP address is the address assigned to the machine within a local network
    (typically something like 192.168.x.x or 10.x.x.x), as opposed to the global IP 
    address used for internet communication. This method uses the `socket` library to 
    obtain the local IP address of the machine running the code.
    """
    return gethostbyname(gethostname())


def get_device(request: HttpRequest) -> StopIteration:
    """
    Determine the type of device connected to the network based on the HTTP request.

    Args:
        request (HttpRequest): The HTTP request containing metadata, including the user agent string.

    Returns:
        str: The type of device (e.g., "Desktop", "Laptop") or "Unknown device" if the type cannot be determined.

    """
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    device            = DeviceDetector(user_agent_string).parse()
    return device.device_type() or "Unknow device"


def hash_data(input_string:str, secret_key:str) -> str:
    """Hash the input string using HMAC and SHA256."""
    
    secret_key_bytes = bytes(secret_key, "utf-8")
    hashed_data      = hmac.new(secret_key_bytes, input_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"hashed__{hashed_data}"


def hash_ip(ip_address:str, secret_key:str) -> hash_data:
    """Hash an IP address using HMAC and SHA256."""
    return hash_data(ip_address, secret_key)