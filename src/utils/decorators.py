from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def is_authorised(view_func):
    """
    Decorator to check if a user has the authorization to access a specific view. 
    If the user is authorized, they are granted access to the view; otherwise, they 
    are redirected to the home page with an informational message.

    Parameters:
    - view_func (function): The view function the user is attempting to access.

    Returns:
    - function: The original view function if the user is authorized; otherwise, 
      a redirection to the home page.
    
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin):
            return view_func(request, *args, **kwargs)
        messages.info(request, "You are not authorised to view that page. You have been redirected to the home page.")
        return redirect("home")
        
    return wrapper
