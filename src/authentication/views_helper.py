from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.http import HttpRequest

from authentication.models import UserBaseLineData, UserDevice, User
from utils.generator import generate_token, generate_verification_url
from utils.validator import is_ip_address_valid
from utils.custom_errors import IPAddressError
from utils.validator import validate_required_keys
from utils.distance_calculator import is_travel_impossible
from utils.utils import get_device, hash_ip
from utils.tasks import notify_user_of_suspicious_login, notify_user_of_different_browser_login

from os import getenv
from dotenv import load_dotenv

import requests
import logging



logger = logging.getLogger('custom_logger')


# Enables the `.env` file to be loaded
load_dotenv()

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


def is_suspicious_login(ip_address, user_baseline_data):
    """
    Checks if the login attempt appears suspicious based on the geo-location data.

    Args:
        ip_address (str): The IP address of the client.
        user_baseline_data (dict): The baseline data for the user, containing "latitude", "longitude", and "timestamp".

    Returns:
        tuple: (bool, str) where the first value is True if login is valid, False otherwise,
               and the second value is an error message if suspicious.
    """
  
    AIRPLANE_SPEED_KMH = 900
    REQUIRED_KEYS      = ["latitude", "longitude", "timestamp"]

    # Validate baseline data
    if not user_baseline_data or not isinstance(user_baseline_data, dict):
        logger.error(f"Invalid baseline data provided to the is_supicious_login function: {user_baseline_data}")
        return False, "Invalid baseline data."

    try:
        validate_required_keys(user_baseline_data, REQUIRED_KEYS)
    except KeyError as e:
        logger.error(f"Invalid - {e}")
        return False, "Missing keys for the user baseline data"

    # Retrieve current geo-location
    try:
        
        current_geo_location = get_cached_geo_location_or_from_ip(ip_address)
        
        if not current_geo_location:
            logger.error("Missing the current geo location data")
            return False, "Missing the current geo-location data"
        
        loc = current_geo_location.get("loc")
        
        if not loc or "," not in loc:
            logger.error(f"Invalid 'loc' format in current_geo_location. Data: {current_geo_location}")
            return False, "Invalid current_geo_location dictionary"
        
        latitude, longitude = map(float, loc.split(","))
        
        timestamp = current_geo_location.get("timestamp")
        
        if not timestamp:
            logger.error(f"Invalid 'timestamp' not found in the current geo location. Data: {current_geo_location}")
            return False, "The timestamp wasn't found"

        current_coordinates = {
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": current_geo_location.get("timestamp"),
        }
        
        if not is_travel_impossible(user_baseline_data, current_coordinates, AIRPLANE_SPEED_KMH):
            return False, "We detected an unusual login attempt and have temporarily blocked access for your security. Please verify your identity or contact support for assistance."
        return True, ""
    
    except ValueError as e:
        error = str(e)
        logger.error(f"Failed to retrieve location data: {error}")
        return False, error


def get_cached_geo_location_or_from_ip(ip_address):
    """
    Retrieves the geo-location from the cache using the ip address. 
    If geo-location is not found, the ip-address is used to retrieved
    the geo-location, stored and then returned to the user. If the 
    geo-location cannot be retrieve a value of None is returned.
    
    Args:
        ip_address (str): The ip address that will be used to return the geo-location.
    
    Returns:
        - A dictionary containing the geo-location 
            {
                "latitude": 51.50853, 
                "!ongitude": -0.12574,
                "timestamp": 0.12985288
            }
        
        - None if the geo-location cannot be retrieved using the ip-address
    """
    key              = f"client_ip_geo_location_{ip_address}"
    ONE_HOUR_IN_SECS = 3600
    geo_location     = cache.get(key)
    
    if geo_location:
        print("Getting from cache...")
        return geo_location
    
    current_geo_location = _get_location_from_ip(ip_address)
    print("Retrieving geo-location data from a new request...")
        
    if not current_geo_location:
        logger.error(f"The current geo location for the {ip_address} couldn't be retrieved")
        return None
        
    current_geo_location["timestamp"] = timezone.now()
        
    cache.set(key=key, value=current_geo_location, timeout=ONE_HOUR_IN_SECS)
    return current_geo_location


def _get_location_from_ip(ip_address):
    """
    Takes either IPV4 or IPV6 ip address and returns the geolocation data using the ipinfo.io API
        
    Args:
        ip_address (str): An ipv4 or ipv6 address that will be used to retrieve the location data.
        
    :Raises
        Raise `IPAddressError` if the ip address provided or the API is invalid.
           
    :Returns
        Returns a dictionary containing the geo-location data. The dictionary contains the following info:
            - ip
            - hostname
            - city
            - region
            - country
            - loc (latitude, longitude)
            - org
            - postal
            - timezone
            
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


def validate_user_status(user):
    
    error_msg = ""
    is_valid  = True
    
    if user.is_banned:
        error_msg = "Your account has been banned, please contact support."
        is_valid  = False
    elif not user.is_active:
        error_msg = "Your account is no longer active, please contact support."
        is_valid  = False
        
    return is_valid, error_msg


def get_user_baseline_data(ip_address: str, user: User) -> UserBaseLineData:
    """
    Takes either IPV4 or IPV6 ip address and a user and returns the UserBaseLineData model associated with
    that IP.
    
    Returns None if not found.
    
    Args:
        ip_address (str): An ipv4 or ipv6 address that will be used to retrieve the UserBaseLineData model.
    
    Returns:
        UserBaseLineData model | None:
    
    """
    ip_address = hash_ip(ip_address, getenv("SECRET_KEY"))
    return UserBaseLineData.get_by_ip_address_and_user(ip_address=ip_address, user=user)


def extract_coordinates(data):
    """
    Extracts a set of geo-coordinates from a an object.
    
    Returns None if the geo-coordinates are not found in the object
    
    Args:
        - data (obj): An object containing a set of coordinates
    
    Returns:
        dict | None :  Returns a dictionary containing the following coordinates `latitude`, `longitude` and `timestamp` 
                       none if not found
    """
    try:
        return {
            "latitude":  data.latitude,
            "longitude": data.longitude,
            "timestamp": data.timestamp,
        }
    except ValueError:
        logger.error(f"Failed to extract the necessary coordiantes from the data:  {data}")
        return None
    

def process_user_device(user:User, user_device_info:dict, request:HttpRequest, ip_address:str, baseline_data:UserBaseLineData) -> True:
    """
    Determines whether the login device used is the same as the one used during registration.
    
    If the devices are not the same, the user is informed by email otherwise nothing is done.
    
    Args:
        user (user obj): The user object that will be used to extract the particular device belonging to the user
        user_device_info (dict): The user device attribrutes captured at login. This data will be compared against
                            the baseline user device captured at registration.
       request (HttpRequest): Contains the user HTTP request for additonal information.
       baseline_data (UserBaseLineData): The user Baseline data object
    
    Returns:
        Returns True
    """
    SECRET_KEY                 = getenv("SECRET_KEY")
    existing_device            = UserDevice.get_by_user(user=user)
    is_same_device             = True
    device                     = get_device(request),
    user_device_info["device"] = str(device)
    
    if not existing_device:
        UserDevice.objects.create(
            user=user,
            frontend_timezone=user_device_info.get("timeZone"),
            user_agent=user_device_info.get("userAgent"),
            screen_width=user_device_info.get("screenWidth"),
            screen_height=user_device_info.get("screenHeight"),
            is_touch_device=user_device_info.get("isDeviceTouchScreen"),
            platform=user_device_info.get("platform"),
            browser=user_device_info.get("browser"),
            browser_version=user_device_info.get("browserVersion"),
            device=device,
            pixel_ratio=user_device_info.get("pixelRatio"),
        )
     
    if existing_device:
        is_same_device = is_same_device_check(existing_device, user_device_info)
     
    if hash_ip(ip_address, SECRET_KEY) != baseline_data.client_ip_address or not is_same_device:
        handle_different_browser_login(user, user_device_info, ip_address)
        
    return True


def handle_suspicious_login(user:User, user_device_info:dict, ip_address:str):
    """Notify user of a suspicious login attempt."""
    
    logger.warning(f"Suspicious login detected for user {user.id} from IP {ip_address}.")
    
    subject = "We Blocked a Suspicious Login to Protect Your Account"
    notify_user_of_suspicious_login(subject, user, user_device_info, ip_address)


def handle_different_browser_login(user:User, user_device_info:dict, ip_address:str):
    """Notify user of a login from a different browser."""
    
    logger.warning(f"Detected that the user is using a different browser or device {user.id} from IP {ip_address}.")
    
    subject = "We noticed you logged in from a different browser"
    notify_user_of_different_browser_login(subject, user, user_device_info, ip_address)
    

def is_same_device_check(existing_device:UserDevice, user_device_info:dict):
    """Check if the login comes from the same device."""
    
    frontend_timezone_match = existing_device.frontend_timezone == user_device_info.get("timeZone")
    screen_width_match      = existing_device.screen_width      == user_device_info.get("screenWidth")
    user_agent_match        = existing_device.user_agent        == user_device_info.get("userAgent")
    screen_height_match     = existing_device.screen_height     == user_device_info.get("screenHeight")
    is_touch_device_match   = existing_device.is_touch_device   == user_device_info.get("isDeviceTouchScreen")
    platform_match          = existing_device.platform          == user_device_info.get("platform")
    browser_match           = existing_device.browser           == user_device_info.get("browser")
    browser_version_match   = existing_device.browser_version   == user_device_info.get("browserVersion")
    pixel_ratio_match       = existing_device.pixel_ratio       == user_device_info.get("pixelRatio")
    device_match            = existing_device.device            == user_device_info.get("device")

    # Check if all conditions match
    all_match = all([frontend_timezone_match, 
                     screen_width_match, 
                     user_agent_match, 
                     screen_height_match, 
                     is_touch_device_match,
                     platform_match, 
                     browser_match, 
                     browser_version_match, 
                     pixel_ratio_match,
                     device_match
                     ]
                    )
    
    return all_match