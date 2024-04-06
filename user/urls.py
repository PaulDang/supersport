from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("cart/", views.cart, name="cart"),
    path("signin/", views.get_signin, name="signin"),
    path("signup/", views.get_signup, name="signup"),
    path("signout/", views.get_signout, name= "signout"),
]
