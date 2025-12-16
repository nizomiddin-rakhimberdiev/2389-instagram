from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

# Create your views here.
def login_view(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html')

def profile_view(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'profile.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(username=username, email=email, phone=phone, password=password)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')