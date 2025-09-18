from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import LoginAttempt
from django.utils import timezone
from datetime import timedelta

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ip_address = get_client_ip(request)

            # Brute-force check
            recent_failures = LoginAttempt.objects.filter(
                username=username,
                timestamp__gte=timezone.now() - timedelta(minutes=15)
            ).count()

            if recent_failures >= 5:
                messages.error(request, 'This account is temporarily locked due to too many failed login attempts. Please try again later.')
                return render(request, 'accounts/login.html', {'form': form})

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Clear failed attempts for this user on successful login
                LoginAttempt.objects.filter(username=username).delete()
                return redirect('dashboard')
            else:
                # Log failed attempt
                LoginAttempt.objects.create(username=username, ip_address=ip_address)
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
