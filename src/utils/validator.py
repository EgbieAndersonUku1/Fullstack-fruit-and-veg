from django.core.validators import validate_email
from django.core.exceptions import ValidationError



def validate_email(email):
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
          
    