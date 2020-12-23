from django.shortcuts import redirect

def cant_use_when_logged(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper
'''
def staff_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper
'''