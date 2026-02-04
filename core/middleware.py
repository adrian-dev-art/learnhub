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
                resolved = resolve(request.path_info)
                current_url_name = resolved.url_name
                current_namespace = resolved.namespace

                # Don't redirect if we are in the admin namespace
                if current_namespace == 'admin':
                    return self.get_response(request)

                if current_url_name in restricted_url_names:
                    if request.user.role == 'admin':
                        return redirect('admin_dashboard')
                    if request.user.is_mentor or request.user.role == 'penulis':
                        return redirect('mentor_dashboard')
                    return redirect('student_dashboard')
            except:
                pass

        response = self.get_response(request)
        return response
