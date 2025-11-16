# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role,
            phone_number=phone_number,
            address=address,
        )

        messages.success(request, "Account created successfully!")
        login(request, user)   # Auto login after registration
        return redirect("home")   # Change to your homepage URL name

    return render(request, "auth/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")   # redirect to dashboard/home
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "auth/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

