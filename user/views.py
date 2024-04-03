from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def cart(request):
    template = loader.get_template("cart.html")
    return HttpResponse(template.render())


def main(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


def get_signup(request):
    template = loader.get_template("signup.html")
    return TemplateResponse(request, template)


# Checking login user
def get_signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect("home")
        else:
            messages.error(request, "Fail logged in")
            return redirect("home")
    else:
        template = loader.get_template("signin.html")
        return TemplateResponse(request, template)
