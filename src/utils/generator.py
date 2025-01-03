from secrets import token_urlsafe

from utils.utils import get_image_extenstion


def generate_token():
    """Generates a url safe token"""
    return token_urlsafe()



def generate_verification_url(request, user):
    """
    Generate a verification URL using the current request host and user's email verification data.

    Args:
        request (HttpRequest): The current HTTP request object.
        user (User): The user instance.

    Returns:
        str: The complete verification URL.
    """
    return _generate_url(
        request=request,
        user=user,
        verification_key="email_verification",
        path="authentication/verify"
    )


def generate_forgotten_password_url(request, user):
    """
    Generate a verification URL for the user's forgotten password process.

    Args:
        request (HttpRequest): The current HTTP request object.
        user (User): The user instance.

    Returns:
        str: The complete verification URL.
    """
    return _generate_url(
        request=request,
        user=user,
        verification_key="forgotten_password_verification_code",
        path="authentication/new/forgotten_password"
    )



def _generate_url(request, user, verification_key, path):
    """
    Private function to generate the verification URL for the user based on the request and verification key.

    Args:
        request (HttpRequest): The current HTTP request object.
        user (User): The user instance.
        verification_key (str): The key to fetch the user's verification code.
        path (str): The URL path for the verification.

    Returns:
        str: The complete verification URL.
    """
    # Clean the path to ensure no leading or trailing slashes
    path = path.strip("/")

    token = user.verification_data.get(verification_key, {}).get("verification_code")
    if not token:
        raise ValueError(f"Verification code for {verification_key} not found.")
    
    current_site = request.get_host()
    protocol     = 'https' if request.is_secure() else 'http'
    
    return f"{protocol}://{current_site}/{path}/{user.username}/{token}/"


def generate_random_image_filename(base_image_name, image, basefolder=None):
      
    extenstion         = get_image_extenstion(image)
    generated_filename = ""
    
    if basefolder:
         basefolder = basefolder[:-1] if basefolder.endswith("/") else basefolder
         generated_filename = f'product_images/{generate_token()}_{base_image_name}.{extenstion}'
    else:
        generated_filename = f'{generate_token()}_{base_image_name}.{extenstion}'
    return generated_filename
    