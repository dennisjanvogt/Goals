# goals/goals/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from tracking import views_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracking/', include('tracking.urls')),
    path('todo/', include('todo.urls')),
    path('register/', views_auth.register_view, name='register'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('home.urls')),  # Include home urls for landing page
    path('', lambda request: redirect('goals'), name='home'),
]

