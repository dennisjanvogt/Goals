# tracking/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Exclude login, logout, and register pages
            allowed_paths = [
                reverse('login'),
                reverse('logout'),
                reverse('register'),
                '/admin/',
            ]
            
            # Check if the current path is in the allowed paths
            if not any(request.path.startswith(path) for path in allowed_paths):
                return redirect(f"{reverse('login')}?next={request.path}")
                
        response = self.get_response(request)
        return response