from django.http import HttpRequest  
from typing import Optional


from utils.generator import generate_token



def set_session(request, session_name: str, email: Optional[str] = None):
    """
    Sets a session value for the given user and session name.

    Args:
        request (HttpRequest): The HTTP request object.
        session_name (str): The purpose or name of the session key.
        email (str, optional): The user's email. Defaults to the user's email in the request.
    """
    
    if not isinstance(request, HttpRequest): 
        raise TypeError(f"The request must be an instance of HttpRequest - <{type(request).__name__}>")
    
    email       = email or request.user.email
    session_key = f"{request.user.id}_{session_name}"
    
    request.session[session_key] = {
        "email": email,
        "token": generate_token()
    }



def get_session(request, session_name:str):
    """
    Retrieve a session value for the given user and session name.

    Args:
        request (HttpRequest): The HTTP request object.
        session_name (str): The purpose or name of the session key.

    Returns:
        dict or None: The session value if it exists, otherwise None.
    
    Raises:
        TypeError: If the request is not an instance of HttpRequest.
    """
    if not isinstance(request, HttpRequest): 
        raise TypeError(f"The request must be an instance of HttpRequest - <{type(request).__name__}>")
    
    session_key = f"{request.user.id}_{session_name}"
    return request.session.get(session_key, None)  