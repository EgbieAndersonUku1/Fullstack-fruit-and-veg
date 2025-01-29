from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import ipaddress


def validate_email_address(email):
    """
    Takes an email and validate if the email has the right
    format. If the email has an incorrect format returns False
    and True if the format is correct
    
    Params:
        email (str): The email to validate
    
    Returns:
        True if valid or False if not
        
    Example usage:
    
    >>> validate_email(example@gmail.com)
    True
    
    >>> validate_email(example.com)
    False
    """
    try:
        validate_email(email) 
        return True
    except ValidationError:
        return False
          
    
    
def validate_required_keys(context, required_keys):
    """
    Validates that the required keys are present in the context.
    
    :param context: A dictionary containing various details.
    :param required_keys: A list of required keys that must be present in the context.
    :raises KeyError: If any required key is missing.
    
    Example usage:
    >>> context = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
    
    >>> required_keys = ["key1", "key2", "key3"]
    >>> validate_required_keys(context, required_keys)
    >>> True
    
    >>> required_keys = ["key1", "key8", "key3"]
    >>> raises KeyError("Returns a list of missing keys in the form of a string")
      
    """
    missing_keys = [key for key in required_keys if key not in context]
    if missing_keys:
        raise KeyError(f"The following keys are missing in context: {', '.join(missing_keys)}")
    
    
def validate_instance_of(instance, expected_class):
    """
    Validates if the instance is an instance of the expected class.

    :param instance: The object to validate.
    :param expected_class: The class that the instance should be an instance of.
    :raises ValueError: If the instance is not an instance of the expected class.
    """
    if not isinstance(instance, expected_class):
        raise ValueError(
            f"The instance is not of type {expected_class.__name__}. Expected {expected_class.__name__} instance, got {type(instance).__name__}."
        )


def is_ip_address_valid(ip_string):
    """
    Determines if the given string is a valid IPv4 or IPv6 address.

    Args:
        ip_string (str): The IP string to validate.

    Returns:
        bool: True if the IP string is a valid IPv4 or IPv6 address, False otherwise.

    Example Usage:
        >>> print(is_ip_address_valid("192.168.1.1"))  # IPv4, True
        >>> print(is_ip_address_valid("2001:0db8:85a3:0000:0000:8a2e:0370:7334"))  # IPv6, True
        >>> print(is_ip_address_valid("999.999.999.999"))  # Invalid, False
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False
