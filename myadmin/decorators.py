from django.shortcuts import redirect
from django.conf import settings
from functools import wraps

def staff_required(view_func):
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            # User is staff, allow access to the view
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            # User is not staff but authenticated, redirect to customer dashboard
            return redirect('account:customer_dashboard')  # Replace with your customer dashboard URL name
        else:
            # User is not staff and not authenticated, redirect to login page
            return redirect(settings.LOGIN_URL)
    return wrapper
