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
    token            = user.verification_data.get("verification_code")
    current_site     = request.get_host()
    protocol         = 'https' if request.is_secure() else 'http'
    verification_url = f"{protocol}://{current_site}/authentication/verify/{ user.username }/{token}/"
    return verification_url
