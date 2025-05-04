# goals/goals/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from tracking import views_auth

def redirect_to_goals(request):
    # Get all query parameters to preserve them
    query_string = request.META.get('QUERY_STRING', '')
    redirect_url = 'goals'
    if query_string:
        return redirect(f'{redirect_url}?{query_string}')
    return redirect(redirect_url)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracking/', include('tracking.urls')),
    path('todo/', include('todo.urls')),
    path('register/', views_auth.register_view, name='register'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('home.urls')),  # Include home urls for landing page
    path('', redirect_to_goals, name='home'),
]