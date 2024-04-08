from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

User = get_user_model()


def cart(request):
    template = loader.get_template("cart.html")
    return HttpResponse(template.render())


def main(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


def get_signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("main")

        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render(
        request=request,
        template_name="signup.html",
        context={"register_form": form},
    )


def get_signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                print("Current request:", request)
                return redirect("main")

        messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="signin.html", context={"login_form": form}
    )


def get_signout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("signin")

def checkout(request):
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render())