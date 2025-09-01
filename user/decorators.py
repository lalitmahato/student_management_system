from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:user_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if allowed_roles:
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return redirect('user:error_401')
        return wrapper_func
    return decorator
