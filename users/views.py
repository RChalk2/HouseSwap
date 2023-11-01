from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from django.contrib import messages


def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "You have signed up successfully.")
            login(request, user)
            return redirect("update_profile")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})



# from https://www.pythontutorial.net/django-tutorial/django-login/
def sign_in(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "users/login.html", {"form": form, "form.errors": form.errors})


def sign_out(request):
    logout(request)
    messages.success(request, f"You have been logged out.")
    return redirect("home")


def password_reset(request):
    return redirect("home")
