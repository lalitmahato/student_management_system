from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('students:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_groups=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if allowed_groups:
                if group in allowed_groups:
                    return view_func(request, *args, **kwargs)
            return redirect('user:unauthorized')
        return wrapper_func
    return decorator
