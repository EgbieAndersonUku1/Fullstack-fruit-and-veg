import json
from django.conf import settings
from django.contrib import messages

from utils.generator import generate_token, generate_verification_url
from utils.utils import get_local_ip_address


def send_verification_email(request, user, subject, follow_up_message, send_func, generate_verification_url_func=None, **kwargs):
    """
    Sends a verification email using the provided sending function.

    This function generates a new verification code for the user, constructs the verification URL, 
    and sends an email using the specified sending function. It also handles success and error messages 
    based on the email sending response.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - user (User): The user object for whom the email is being sent.
    - subject (str): The subject line of the email.
    - follow_up_message (str): A message to display upon successful email sending.
    - send_func (function): A function responsible for sending the email. This function should accept:
      - `subject` (str): The subject line of the email.
      - `from_email` (str): The sender's email address.
      - `user` (User): The user object, typically containing `user.email` and `user.username`.
      - `verification_url` (str): The URL for completing the verification process.
    - generate_verification_url_func (function, optional): A function that generates the verification URL.
      If None, the default `generate_verification_url` function will be used.

    kwargs:
        - expiry_date (int, optional): Custom expiry duration in minutes. Defaults to 4320 (3 days).
        - verification_key (str, optional): Custom key for storing the verification code. Defaults to "verification_code".

    Returns:
    - bool: True if the email was sent successfully, False otherwise.
    """

    # Handle default values from kwargs
    expiry_minutes   = kwargs.get("expiry_date", 4320)  # Default expiry is 3 days
    verification_key = kwargs.get("verification_key", "verification_code")

    if generate_verification_url_func == None:
        user.set_verification_code(code=generate_token(), expiry_minutes=expiry_minutes, default_key="email_verification")
        verification_url = generate_verification_url(request, user)
     
    else:
        user.set_verification_code(code=generate_token(), expiry_minutes=expiry_minutes, default_key=verification_key)
        verification_url = generate_verification_url_func(request, user)
      
    try:
        email_sent = send_func(
            subject=subject,
            from_email=settings.EMAIL_HOST_USER,
            user=user,
            verification_url=verification_url
        )

        if email_sent:
            messages.success(request, follow_up_message)
        else:
            messages.error(request, "Failed to send email")
            
        return email_sent

    except Exception as e:
        print(e)
        print(verification_url)
        messages.error(request, "An unexpected error occurred while sending the email. Please try again later.")
        return False


def get_client_ip_address(request) -> str:
    """
    Retrieve the IP address of the client making the request.
    
    This function checks the 'X-Forwarded-For' header to get the client's real IP address 
    when the request passes through a proxy. If the header is absent, it falls back to 
    'REMOTE_ADDR'. If the request returned is a localhost (127.0.0.1), the local IP address is returned, 
    which is typically only meaningful within the local network.
    """
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    LOCALHOST       = '127.0.0.1'
    
    if x_forwarded_for:
        # If the request passes through a proxy, the first IP in the list is the real client IP
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    if ip == LOCALHOST:  
        # Get the local ip address if client ip fails
        ip = get_local_ip_address()
    
    return ip
