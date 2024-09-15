
from functools import wraps

from django.shortcuts import render


def is_authorised(view_func):
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        elif request.user.is_staff:
            return render(request, 'access_denied.html', status=403)
        else:
            return render(request, 'access_denied.html', status=403)

    return wrapper