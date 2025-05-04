# goals/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracking import views_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracking/', include('tracking.urls')),
    path('todo/', include('todo.urls')),  # New URL pattern
    path('register/', views_auth.register_view, name='register'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', lambda request: redirect('goals'), name='home'),
]