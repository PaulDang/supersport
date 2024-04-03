from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import loader


def cart(request):
    template = loader.get_template("cart.html")
    return HttpResponse(template.render())


def main(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


def get_signin(request):
    template = loader.get_template("signin.html")
    return TemplateResponse(request, template)


def get_signup(request):
    template = loader.get_template("signup.html")
    return TemplateResponse(request, template)
