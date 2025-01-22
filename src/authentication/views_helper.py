from django.conf import settings
from django.contrib import messages

from utils.generator import generate_token, generate_verification_url
from utils.utils import get_local_ip_address
from utils.validator import is_ip_address_valid
from utils.custom_errors import IPAddressError

from dotenv import load_dotenv
from os import getenv
import requests


# Enables the `.env` file to be loaded
load_dotenv(override=True)

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
    
    if ip == LOCALHOST or getenv("MODE") == "development":  
        
        # In development mode, the system returns the localhost IP address (127.0.0.1).
        # This is due to the fact that requests in development are typically made from the same machine, so the IP address is local.
        # In such cases, the user global IP address is fetched from the CLIENT_IP_ADDRESS variable in the .env file to ensure
        # the rest of the application functions as expected.
        ip = getenv("CLIENT_IP_ADDRESS")
        
        if not is_ip_address_valid(ip):
            raise IPAddressError(f"The ip address <{ip}> retrieved from the .env is not a valid ip address. IP address must either be an IPV4 or IPV6")
      
    return ip


def get_location_from_ip(ip_address):
    """
    Takes either IPV4 or IPV6 ip address and returns the geolocation data using the ipinfo.io API
        
    Args:
        ip_address (str): An ipv4 or ipv6 address that will be used to retrieve the location data.
        
    :Raises
        Raise `IPAddressError` if the ip address provided or the API is invalid.
           
    :Returns
        Returns a dictionary containing the geo-location data. The dictionary contains the following info:
            - IP
            - Hostname
            - City
            - Region
            - Country
            - loc (latitude, longitude)
            - org
            - Postal
            - Timezone
            
    """
    if not is_ip_address_valid(ip_address):
        raise IPAddressError("The ip address <{ip_address}> does not appear to be an IPv4 or IPv6 address")
    
    API_KEY  = getenv("IPINFO_API_KEY")
   
    if not API_KEY:
        raise IPAddressError("IPINFO_API_KEY is not set in environment variables.")
    
    URL = f"https://ipinfo.io/{ip_address}?token={API_KEY}"
    
    try:
        response = requests.get(URL)
        
        if not response.ok:
            raise IPAddressError(f"Failed to retrieve location for IP address <{ip_address}>. API returned status code {response.status_code}.")
        
        location = response.json()
        return location
    except requests.exceptions.RequestException as e:
        raise IPAddressError(f"An error occurred while attempting to fetch data for IP address <{ip_address}>: {e}")
