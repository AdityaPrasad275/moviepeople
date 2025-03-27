from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from .forms import UserSearchForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("users:login")
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserCreationForm()

    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")  # You'll create this view later
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("users:login")


@login_required
def profile_view(request, username=None):
    if username:
        # View another user's profile
        profile_user = get_object_or_404(User, username=username)
    else:
        # View own profile
        profile_user = request.user

    return render(request, "users/profile.html", {"profile_user": profile_user})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "users/edit_profile.html", {"form": form})


def search_users(request):
    User  # Get the currently active user model
    form = UserSearchForm(request.GET or None)
    users = []

    if form.is_valid() and any(form.cleaned_data.values()):
        username_query = form.cleaned_data.get("username", "")
        role = form.cleaned_data.get("role", "")
        location = form.cleaned_data.get("location", "")

        # Start with all users except the current user
        users_query = User.objects.exclude(id=request.user.id)

        # Apply filters
        if username_query:
            users_query = users_query.filter(
                Q(username__icontains=username_query)
                | Q(email__icontains=username_query)
            )

        if role:
            users_query = users_query.filter(profile__role__icontains=role)

        if location:
            users_query = users_query.filter(profile__location__icontains=location)

        users = users_query.distinct()

    return render(request, "users/search_results.html", {"form": form, "users": users})
