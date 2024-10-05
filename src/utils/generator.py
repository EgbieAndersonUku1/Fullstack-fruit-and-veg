from secrets import token_urlsafe


def generate_token():
    """Generates a url safe token"""
    return token_urlsafe()




def generate_verification_url(request, user):
    """
    Generate a verification URL using the current request host and user model.

    Args:
        request (HttpRequest): The current HTTP request object.
        user (str): The user model.

    Returns:
        str: The complete verification URL.
    """
    
    verification_data = user.verification_data.get("email_verification", {})
    current_site      = request.get_host()
    protocol          = 'https' if request.is_secure() else 'http'
    verification_url  = f"{protocol}://{current_site}/authentication/verify/{ user.username }/{verification_data.get("verification_code")}/"
    return verification_url


def generate_forgotten_password_url(request, user):
    """
    Generate a verification URL for the user forgotten password

    Args:
        request (HttpRequest): The current HTTP request object.
        user (str): The user model.

    Returns:
        str: The complete verification URL.
    """
    token            = user.verification_data.get("forgotten_password_verification_code").get("verification_code")
    current_site     = request.get_host()
    protocol         = 'https' if request.is_secure() else 'http'
    verification_url = f"{protocol}://{current_site}/authentication/verify/forgotten_password/{ user.username }/{token}/"
    return verification_url
