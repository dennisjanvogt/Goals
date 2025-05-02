# tracking/views_auth.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomAuthenticationForm  # Import your custom form

def register_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('goals')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrierung erfolgreich!')
            return redirect('goals')
    else:
        form = UserCreationForm()
    return render(request, 'tracking/auth/register.html', {'form': form})



def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('goals')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)  # Use custom form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'goals')
                messages.success(request, f'Willkommen zurück, {username}!')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()  # Use custom form
    return render(request, 'tracking/auth/login.html', {'form': form})