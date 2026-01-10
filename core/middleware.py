from django.shortcuts import redirect
from django.urls import reverse

class AuthRedirectMiddleware:
    """
    Middleware to redirect authenticated users away from login and register pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URL names to redirect away from
        restricted_url_names = ['login', 'register']

        if request.user.is_authenticated:
            try:
                from django.urls import resolve
                current_url_name = resolve(request.path_info).url_name

                if current_url_name in restricted_url_names:
                    if request.user.is_mentor:
                        return redirect('mentor_dashboard')
                    return redirect('student_dashboard')
            except:
                pass

        response = self.get_response(request)
        return response
